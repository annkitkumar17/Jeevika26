import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { RotateCcw, Volume2, ArrowRight, ArrowLeft } from 'lucide-react';
import { Button } from '../components/ui/Button';
import { ProgressStepper } from '../components/ProgressStepper';
import { ConversationBubble } from '../components/ConversationBubble';
import { VoiceRecorder } from '../components/VoiceRecorder';
import { QuickReplyChips } from '../components/QuickReplyChips';
import { ConfirmDialog } from '../components/ConfirmDialog';
import { DemoDataBadge } from '../components/DemoDataBadge';
import { INTERVIEW_QUESTIONS } from '../lib/constants';
import { useAppStore } from '../stores/useAppStore';
import { useRecommendations } from '../hooks/useRecommendations';
import { useVoiceSession } from '../hooks/useVoiceSession';

export const Conversation: React.FC = () => {
  const navigate = useNavigate();
  const {
    currentQuestionIndex,
    answers,
    messages,
    language,
    setAnswer,
    addMessage,
    confirmMessage,
    editMessage,
    nextQuestion,
    prevQuestion,
    resetConversation,
  } = useAppStore();

  const { generateProfile, isGeneratingProfile } = useRecommendations();
  const { speakText, isPlayingQuestion } = useVoiceSession();

  const [showResetModal, setShowResetModal] = useState(false);

  const currentQ = INTERVIEW_QUESTIONS[currentQuestionIndex] || INTERVIEW_QUESTIONS[0];
  const isHindi = language === 'hi';
  const promptText = isHindi ? currentQ.promptHi : currentQ.promptEn;
  const chips = isHindi ? currentQ.quickChipsHi : currentQ.quickChipsEn;

  // Initialize first question message if messages empty
  useEffect(() => {
    if (messages.length === 0) {
      addMessage({
        id: `assistant-${currentQ.id}`,
        sender: 'assistant',
        text: promptText,
        timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      });
    }
  }, [currentQuestionIndex]);

  const handleUserAnswer = async (answerText: string) => {
    // Record user answer
    setAnswer(currentQ.key, answerText);

    // Add user message
    const userMsgId = `user-${Date.now()}`;
    addMessage({
      id: userMsgId,
      sender: 'user',
      text: answerText,
      timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      isConfirmed: false,
    });

    // Check if interview is finished
    if (currentQuestionIndex + 1 >= INTERVIEW_QUESTIONS.length) {
      // Final question answered - generate profile
      const finalAnswers = { ...answers, [currentQ.key]: answerText };
      try {
        await generateProfile(finalAnswers);
        navigate('/profile-review');
      } catch (err) {
        navigate('/profile-review');
      }
    } else {
      // Advance to next question
      nextQuestion();
      const nextQ = INTERVIEW_QUESTIONS[currentQuestionIndex + 1];
      const nextPrompt = isHindi ? nextQ.promptHi : nextQ.promptEn;

      setTimeout(() => {
        addMessage({
          id: `assistant-${nextQ.id}`,
          sender: 'assistant',
          text: nextPrompt,
          timestamp: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        });
      }, 400);
    }
  };

  const handleRestart = () => {
    resetConversation();
    window.location.reload();
  };

  return (
    <div className="max-w-4xl mx-auto py-6 px-4 space-y-6">
      {/* HEADER & STEPPER */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-4 rounded-2xl bg-white border border-slate-200 shadow-sm">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <h1 className="text-xl font-bold text-slate-900">Guided Voice Interview</h1>
            <DemoDataBadge text="Simulated NLP" className="py-0 px-2 text-[10px]" />
          </div>
          <p className="text-xs text-slate-500">
            Est. time remaining: ~{(INTERVIEW_QUESTIONS.length - currentQuestionIndex) * 0.5} mins
          </p>
        </div>

        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            onClick={() => speakText(promptText, isHindi ? 'hi-IN' : 'en-US')}
            className="gap-1.5 text-xs"
          >
            <Volume2 className={`h-4 w-4 ${isPlayingQuestion ? 'text-brand-600 animate-pulse' : ''}`} />
            <span>{isPlayingQuestion ? 'Playing...' : 'Play Question'}</span>
          </Button>

          <Button
            variant="ghost"
            size="sm"
            onClick={() => setShowResetModal(true)}
            className="gap-1.5 text-xs text-slate-500 hover:text-rose-600"
          >
            <RotateCcw className="h-3.5 w-3.5" />
            <span>Restart Demo</span>
          </Button>
        </div>
      </div>

      <ProgressStepper
        steps={INTERVIEW_QUESTIONS.map((q) => ({ title: q.key }))}
        currentStepIndex={currentQuestionIndex}
      />

      {/* CHAT TRANSCRIPT CONTAINER */}
      <div className="min-h-[320px] max-h-[460px] overflow-y-auto p-4 rounded-2xl bg-slate-100/70 border border-slate-200 space-y-4">
        {messages.map((msg) => (
          <ConversationBubble
            key={msg.id}
            message={msg}
            onConfirm={(id) => confirmMessage(id)}
            onEdit={(id, newText) => editMessage(id, newText)}
            onPlayAudio={(text) => speakText(text, isHindi ? 'hi-IN' : 'en-US')}
          />
        ))}

        {isGeneratingProfile && (
          <div className="p-4 rounded-xl bg-brand-50 border border-brand-200 text-brand-900 text-xs font-semibold flex items-center gap-3 animate-pulse">
            <span className="h-2.5 w-2.5 rounded-full bg-brand-600" />
            <span>Generating NSQF-aligned profile from your voice interview answers...</span>
          </div>
        )}
      </div>

      {/* QUICK CHIPS */}
      <QuickReplyChips chips={chips} onSelect={handleUserAnswer} />

      {/* VOICE RECORDER / INPUT CONTROLS */}
      <VoiceRecorder
        onRecorded={handleUserAnswer}
        defaultSimulatedText={chips[0] || 'मैंने सिलाई और मशीन मरम्मत का काम किया है।'}
      />

      {/* BACK & NAVIGATION ACTIONS */}
      <div className="flex justify-between items-center pt-2">
        <Button
          variant="secondary"
          size="sm"
          onClick={prevQuestion}
          disabled={currentQuestionIndex === 0}
          className="gap-1 text-xs"
        >
          <ArrowLeft className="h-3.5 w-3.5" />
          <span>Previous Question</span>
        </Button>

        <span className="text-xs text-slate-400 font-medium">
          Question {currentQuestionIndex + 1} of {INTERVIEW_QUESTIONS.length}
        </span>
      </div>

      {/* CONFIRM RESTART MODAL */}
      <ConfirmDialog
        isOpen={showResetModal}
        onClose={() => setShowResetModal(false)}
        onConfirm={handleRestart}
        title="Restart Voice Interview?"
        description="This will clear your recorded answers and chat transcript in local storage."
        confirmText="Yes, Restart"
      />
    </div>
  );
};
