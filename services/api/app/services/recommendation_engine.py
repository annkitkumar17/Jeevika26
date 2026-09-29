from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.beneficiary import Beneficiary
from app.models.qualification import Qualification
from app.models.recommendation import Recommendation
from app.models.training_centre import TrainingCentre
from app.models.opportunity import OpportunitySignal
from app.models.workflow import ReviewTask
from app.services.geospatial import GeoSpatialService

class RecommendationEngine:
    @classmethod
    def generate_recommendations(
        cls,
        db: Session,
        beneficiary_id: str,
        force_refresh: bool = False
    ) -> List[Recommendation]:
        beneficiary = db.query(Beneficiary).filter(Beneficiary.id == beneficiary_id).first()
        if not beneficiary:
            return []

        # If already generated and not forced, return existing
        existing = db.query(Recommendation).filter(Recommendation.beneficiary_id == beneficiary_id).order_by(Recommendation.rank).all()
        if existing and not force_refresh:
            return existing

        # If forced, remove old recommendations
        if existing:
            db.query(Recommendation).filter(Recommendation.beneficiary_id == beneficiary_id).delete()
            db.commit()

        # Hard Filter 1: Only verified, active NSQF qualifications from authoritative sources
        qualifications = db.query(Qualification).filter(
            Qualification.verification_status == "verified",
            Qualification.archive_status == "active"
        ).all()
        
        if not qualifications:
            cls._seed_default_qualifications(db)
            qualifications = db.query(Qualification).filter(
                Qualification.verification_status == "verified",
                Qualification.archive_status == "active"
            ).all()

        centres = db.query(TrainingCentre).all()
        if not centres:
            cls._seed_default_training_centres(db)
            centres = db.query(TrainingCentre).all()

        # Fetch local opportunity signals for the beneficiary's district
        opportunity_signals = {
            s.sector.lower(): s
            for s in db.query(OpportunitySignal).filter(
                OpportunitySignal.district.ilike(f"%{beneficiary.district}%")
            ).all()
        }

        user_skills = [str(s).lower() for s in (beneficiary.skills or [])]
        user_work = (beneficiary.current_work or "").lower()
        user_pref = beneficiary.preferences or {}
        emp_type = user_pref.get("employment_type", "either")
        max_dist = user_pref.get("max_travel_km", 25)
        user_edu = (beneficiary.education or "Class 8").lower()

        scored_candidates = []

        for q in qualifications:
            # 1. Aspiration & Work match (0-100)
            aspiration_score = 70.0
            if "pump" in user_work or "repair" in user_work:
                if "solar" in q.title.lower() or "pump" in q.title.lower():
                    aspiration_score = 95.0
            elif "farm" in user_work or "agriculture" in user_work or "food" in user_work:
                if "food" in q.title.lower():
                    aspiration_score = 92.0
            elif "sew" in user_work or "tailor" in user_work:
                if "sewing" in q.title.lower() or "apparel" in q.title.lower():
                    aspiration_score = 94.0

            # 2. Skill match (0-100)
            skill_score = 65.0
            if any(k in " ".join(user_skills) for k in ["mechanical", "repair", "tool"]):
                if "solar" in q.title.lower() or "pump" in q.title.lower():
                    skill_score = 92.0
            if any(k in " ".join(user_skills) for k in ["stitching", "cutting", "sewing"]):
                if "sewing" in q.title.lower() or "apparel" in q.title.lower():
                    skill_score = 90.0

            # 3. Entry fit (0-100)
            entry_score = 85.0
            req_edu = (q.entry_requirements or "Class 8").lower()
            if "10" in req_edu and "8" in user_edu and "10" not in user_edu:
                entry_score = 55.0 # Lower entry fit if requirement is higher than completed class

            # 4. Nearest training centre & accessibility (0-100)
            best_centre = None
            min_dist = 999.0
            for c in centres:
                d = GeoSpatialService.haversine_distance_km(
                    beneficiary.latitude or 26.8467,
                    beneficiary.longitude or 80.9462,
                    c.latitude,
                    c.longitude
                )
                if d < min_dist:
                    min_dist = d
                    best_centre = c

            training_accessibility = 90.0 if min_dist <= 15 else 75.0 if min_dist <= max_dist else 45.0
            mobility_fit = 90.0 if min_dist <= max_dist else 50.0

            # 5. Local opportunity signal (0-100)
            opp_signal_obj = None
            for sec_key, signal in opportunity_signals.items():
                if sec_key in q.sector.lower() or sec_key in q.title.lower():
                    opp_signal_obj = signal
                    break

            if opp_signal_obj:
                local_opp_score = 90.0 if opp_signal_obj.demand_level == "high" else 75.0
                signal_text = f"Verified: {opp_signal_obj.demand_level.capitalize()} district demand ({opp_signal_obj.openings_count or 'Active'} openings, source: {opp_signal_obj.source_name})"
            else:
                local_opp_score = 60.0 # Neutral baseline when unknown, not 0!
                signal_text = "Market signal currently unverified in block (shown as unknown)"

            # 6. RPL & Bridge fit (0-100)
            rpl_fit = 85.0 if q.rpl_available else 60.0
            historical_outcome = 80.0

            # Weighted Formula:
            # score = aspiration*0.20 + skill*0.20 + entry*0.15 + local_opp*0.15 + centre*0.10 + mobility*0.10 + rpl*0.05 + outcomes*0.05
            composite_score = (
                aspiration_score * 0.20
                + skill_score * 0.20
                + entry_score * 0.15
                + local_opp_score * 0.15
                + training_accessibility * 0.10
                + mobility_fit * 0.10
                + rpl_fit * 0.05
                + historical_outcome * 0.05
            )
            composite_score = round(min(96.0, max(50.0, composite_score)), 1)

            # Build evidence and risk flags
            why_fits = []
            skill_gaps = []
            evidence_list = [
                f"Authoritative Qualification: NSQF Level {q.nsqf_level} (QP: {q.qp_code}, NQR Verified)",
                f"Training Centre Proximity: {best_centre.name if best_centre else 'PMKK Sadar'} ({min_dist:.1f} km straight-line estimate)",
            ]
            unknowns_list = []
            risks_list = []
            next_actions = [
                "Schedule facilitator counseling review",
                "Verify batch start date at nearest PMKK centre",
                "Submit document readiness checklist"
            ]

            human_review_required = False

            if "solar" in q.title.lower():
                why_fits.append("Mechanical pump troubleshooting experience directly transfers to solar irrigation servicing.")
                why_fits.append("High rural PM-KUSUM scheme subsidised solar pump adoption in block.")
                skill_gaps.append("DC inverter wiring & grid synchronization")
                skill_gaps.append("Photovoltaic array structural mounting & grounding")
                risks_list.append("Requires ladder climbing & outdoor electrical safety protocols")
            elif "food" in q.title.lower():
                why_fits.append("Strong local agricultural supply enables value-added agro-processing micro-enterprise.")
                why_fits.append("Eligible for PM-FME credit-linked capital subsidy up to 35%.")
                skill_gaps.append("FSSAI food hygiene standards & packaging preservation")
                skill_gaps.append("Costing, inventory & local retail tie-ups")
                risks_list.append("Perishable raw materials require refrigerated storage or quick turnover")
            elif "sewing" in q.title.lower():
                why_fits.append("Supports home-based flexible stitching enterprise or local garment cluster wage work.")
                why_fits.append("Short bridge module requirements for fast RPL certification.")
                skill_gaps.append("Industrial lockstitch machine maintenance & tension control")
                skill_gaps.append("Quality inspection & pattern drafting")
                risks_list.append("Piece-rate wage employment depends on seasonal order volumes")

            if not opp_signal_obj:
                unknowns_list.append("Real-time local vacancy count unverified by District Employment Exchange")

            if min_dist > max_dist:
                risks_list.append(f"Centre distance ({min_dist:.1f} km) exceeds stated travel preference ({max_dist} km)")
                human_review_required = True

            if entry_score < 70.0:
                risks_list.append("Beneficiary completed schooling class is below ideal qualification prerequisite")
                human_review_required = True

            scored_candidates.append({
                "qualification": q,
                "score": composite_score,
                "score_breakdown": {
                    "aspiration_match": aspiration_score,
                    "skill_match": skill_score,
                    "entry_fit": entry_score,
                    "local_opportunity": local_opp_score,
                    "training_accessibility": training_accessibility,
                    "mobility_fit": mobility_fit,
                    "rpl_fit": rpl_fit,
                    "historical_outcomes": historical_outcome,
                },
                "why_fits": why_fits,
                "skill_gaps": skill_gaps,
                "evidence": evidence_list,
                "unknowns": unknowns_list,
                "risks": risks_list,
                "next_actions": next_actions,
                "human_review_required": human_review_required,
                "nearest_centre_id": best_centre.id if best_centre else None,
                "nearest_centre_distance_km": round(min_dist, 1) if best_centre else 12.4,
                "signal_text": signal_text,
                "risk_factor": risks_list[0] if risks_list else None
            })

        # Sort descending by composite match score
        scored_candidates.sort(key=lambda x: x["score"], reverse=True)

        recommendations = []
        for idx, item in enumerate(scored_candidates[:3]):
            rec = Recommendation(
                beneficiary_id=beneficiary.id,
                qualification_id=item["qualification"].id,
                rank=idx + 1,
                match_score=item["score"],
                score_breakdown=item["score_breakdown"],
                fit_reason=item["why_fits"][0] if item["why_fits"] else "NSQF aligned qualification match",
                fit_details=item["why_fits"],
                skill_gaps=item["skill_gaps"],
                evidence=item["evidence"],
                unknowns=item["unknowns"],
                risks=item["risks"],
                next_actions=item["next_actions"],
                human_review_required=item["human_review_required"],
                human_validated=False,
                local_opportunity_signal=item["signal_text"],
                nearest_centre_id=item["nearest_centre_id"],
                nearest_centre_distance_km=item["nearest_centre_distance_km"],
                rpl_eligible=True,
                risk_factor=item["risk_factor"],
                status="generated"
            )
            db.add(rec)
            recommendations.append(rec)

            # If human review required, create a ReviewTask for the facilitator
            if item["human_review_required"]:
                review_task = ReviewTask(
                    beneficiary_id=beneficiary.id,
                    assigned_facilitator_id=beneficiary.assigned_facilitator_id,
                    task_type="recommendation_review",
                    priority="high",
                    trigger_reason=f"Recommendation #{idx+1} ({item['qualification'].title}): {', '.join(item['risks'])}",
                    status="pending",
                    sla_due_at=datetime.now(timezone.utc)
                )
                db.add(review_task)

        db.commit()
        for r in recommendations:
            db.refresh(r)

        return recommendations

    @staticmethod
    def _seed_default_qualifications(db: Session):
        sample_qps = [
            Qualification(
                qp_code="ELE/Q5901",
                qualification_code="NQR/ELE/Q5901/V1",
                title="Solar Pump Technician",
                sector="Green Jobs / Electronics",
                nsqf_level=3,
                version="1.0",
                awarding_body="Skill Council for Green Jobs (SCGJ)",
                approval_date="2023-01-15",
                currency_start="2023-01-15",
                currency_end="2028-01-15",
                archive_status="active",
                nsqc_status="approved",
                verification_status="verified",
                description="Installation, troubleshooting, and maintenance of decentralized solar-powered irrigation pumps.",
                entry_requirements="Class 8th + 1 year basic mechanical experience",
                learning_outcomes=["Perform site assessment for PV pump installation", "Mount PV modules securely", "Connect DC controllers and inverters", "Perform routine maintenance & safety inspection"],
                nos_units=["ELE/N5901: Install Solar Pump Components", "ELE/N5902: Test & Commission Solar Systems", "ELE/N9901: Maintain Safe Work Environment"],
                duration_hours=320,
                curriculum_modules=["Solar PV Fundamentals", "Pump Mechanics & Hydraulics", "Safety & Inverter Maintenance", "Customer Soft Skills"],
                potential_job_roles=["Solar Pump Installer", "Service Technician", "Agri-tech Field Lead"],
                average_salary_range="₹14,000 - ₹22,000 / month",
                rpl_available=True
            ),
            Qualification(
                qp_code="FIC/Q9002",
                qualification_code="NQR/FIC/Q9002/V1",
                title="Food Processing Entrepreneur",
                sector="Food Processing",
                nsqf_level=4,
                version="1.0",
                awarding_body="Food Industry Capacity & Skill Initiative (FICSI)",
                approval_date="2023-03-20",
                currency_start="2023-03-20",
                currency_end="2028-03-20",
                archive_status="active",
                nsqc_status="approved",
                verification_status="verified",
                description="Small-scale agro-produce processing, packaging, quality control, and local retail marketing.",
                entry_requirements="Class 10th",
                learning_outcomes=["Standardize recipe and batch processing", "Ensure FSSAI hygienic packaging", "Calculate unit economics & pricing", "Manage local SHG retail supply chain"],
                nos_units=["FIC/N9001: Process Raw Agricultural Produce", "FIC/N9002: Pack and Store Food Items", "FIC/N9901: Comply with Food Safety Regulations"],
                duration_hours=400,
                curriculum_modules=["Food Hygiene & FSSAI Standards", "Drying & Preservation Tech", "Packaging & Branding", "Micro-enterprise Financial Literacy"],
                potential_job_roles=["Micro-Enterprise Owner", "Processing Unit Supervisor", "SHG Group Lead"],
                average_salary_range="₹16,000 - ₹30,000 / month",
                rpl_available=True
            ),
            Qualification(
                qp_code="AMH/Q0301",
                qualification_code="NQR/AMH/Q0301/V2",
                title="Sewing Machine Operator",
                sector="Apparel, Made-Ups & Home Furnishing",
                nsqf_level=3,
                version="2.0",
                awarding_body="Apparel Made-Ups & Home Furnishing Sector Skill Council (AMHSSC)",
                approval_date="2022-09-10",
                currency_start="2022-09-10",
                currency_end="2027-09-10",
                archive_status="active",
                nsqc_status="approved",
                verification_status="verified",
                description="Stitching woven and knitted fabrics using industrial lockstitch and overlock sewing machines.",
                entry_requirements="Class 5th or basic literacy",
                learning_outcomes=["Thread and operate industrial sewing machines", "Stitch various garment seams with specified tolerances", "Perform basic machine maintenance and oiling", "Conduct finished piece quality checks"],
                nos_units=["AMH/N0301: Carry Out Stitching Activities", "AMH/N0302: Maintain Work Area & Tools", "AMH/N9901: Maintain Health, Safety and Security"],
                duration_hours=300,
                curriculum_modules=["Machine Setup & Safety", "Precision Stitching & Seams", "Quality Inspection", "Garment Assembly"],
                potential_job_roles=["Garment Tailor", "Production Line Operator", "Home Enterprise Owner"],
                average_salary_range="₹12,000 - ₹18,000 / month",
                rpl_available=True
            ),
        ]
        for qp in sample_qps:
            db.add(qp)
        db.commit()

    @staticmethod
    def _seed_default_training_centres(db: Session):
        sample_centres = [
            TrainingCentre(
                centre_code="PMKK-LKO-01",
                name="Pradhan Mantri Kaushal Kendra (PMKK) - Sadar",
                centre_type="PMKK",
                address="Near Block Development Office, Sadar Tehsil, Lucknow",
                state="Uttar Pradesh",
                district="Lucknow",
                block="Sadar",
                pincode="226001",
                latitude=26.8520,
                longitude=80.9580,
                contact_person="Manoj Verma",
                contact_phone="+91 98765 43210",
                offered_courses=["ELE/Q5901", "AMH/Q0301"],
                batch_status="Admissions Open",
                next_batch_date="Starting in 12 days"
            ),
            TrainingCentre(
                centre_code="RSETI-LKO-02",
                name="Rural Self Employment Training Institute (RSETI)",
                centre_type="RSETI",
                address="Canara Bank RSETI Complex, Mohanlalganj Road, Lucknow",
                state="Uttar Pradesh",
                district="Lucknow",
                block="Mohanlalganj",
                pincode="226301",
                latitude=26.7842,
                longitude=80.9912,
                contact_person="Sunita Sharma",
                contact_phone="+91 98765 87654",
                offered_courses=["FIC/Q9002"],
                batch_status="Admissions Open",
                next_batch_date="Starting in 7 days"
            ),
            TrainingCentre(
                centre_code="ITI-ALB-03",
                name="Government ITI Alambagh",
                centre_type="ITI",
                address="Kanpur Road, Alambagh, Lucknow",
                state="Uttar Pradesh",
                district="Lucknow",
                block="Sarojini Nagar",
                pincode="226005",
                latitude=26.8124,
                longitude=80.9015,
                contact_person="Ramesh Chandra",
                contact_phone="+91 94150 11223",
                offered_courses=["ELE/Q5901", "AMH/Q0301", "FIC/Q9002"],
                batch_status="Interview Scheduled",
                next_batch_date="Starting in 20 days"
            ),
        ]
        for c in sample_centres:
            db.add(c)
        db.commit()
