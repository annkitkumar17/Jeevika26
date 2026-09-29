import math
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.training_centre import TrainingCentre

class GeoSpatialService:
    @staticmethod
    def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """
        Calculate great circle distance between two points in kilometers
        """
        r = 6371.0  # Earth radius in kilometers
        d_lat = math.radians(lat2 - lat1)
        d_lon = math.radians(lon2 - lon1)
        
        a = (
            math.sin(d_lat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(d_lon / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return round(r * c, 2)

    @classmethod
    def find_nearby_centres(
        cls,
        db: Session,
        lat: float,
        lon: float,
        radius_km: float = 50.0,
        limit: int = 10,
        course_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        centres = db.query(TrainingCentre).all()
        results = []
        
        for c in centres:
            dist = cls.haversine_distance_km(lat, lon, c.latitude, c.longitude)
            if dist <= radius_km:
                if course_filter:
                    courses = c.offered_courses or []
                    if course_filter not in courses:
                        continue
                centre_dict = {
                    "id": c.id,
                    "centre_code": c.centre_code,
                    "name": c.name,
                    "centre_type": c.centre_type,
                    "address": c.address,
                    "state": c.state,
                    "district": c.district,
                    "block": c.block,
                    "pincode": c.pincode,
                    "latitude": c.latitude,
                    "longitude": c.longitude,
                    "contact_person": c.contact_person,
                    "contact_phone": c.contact_phone,
                    "offered_courses": c.offered_courses,
                    "batch_status": c.batch_status,
                    "next_batch_date": c.next_batch_date,
                    "distance_km": dist,
                    "created_at": c.created_at,
                }
                results.append(centre_dict)
        
        results.sort(key=lambda x: x["distance_km"])
        return results[:limit]
