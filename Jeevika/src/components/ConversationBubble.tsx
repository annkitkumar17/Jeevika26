import React, { useState } from 'react';
import { Volume2, Check, Edit2, Bot, User, Sparkles } from 'lucide-react';
import { Button } from './ui/Button';
import { ChatMessage } from '../types';

interface ConversationBubbleProps {
  message: ChatMessage;
  onConfirm?: (id: string) => void;
  onEdit?: (id: string, newText: string) => void;
  onPlayAudio?: (text: string) => void;
}

export const ConversationBubble: React.FC<ConversationBubbleProps> = ({
  message,
  onConfirm,
  onEdit,
  onPlayAudio,
}) => {
  const isBot = message.sender === 'assistant';
  const [isEditing, setIsEditing] = useState(false);
  const [editText, setEditText] = useState(message.text);

  const handleSaveEdit = () => {
    if (onEdit && editText.trim()) {
      onEdit(message.id, editText.trim());
      setIsEditing(false);
    }
  };

  return (
    <div
      className={`flex items-start gap-3.5 my-4 max-w-2xl transition-all ${
        isBot ? 'mr-auto' : 'ml-auto flex-row-reverse'
      }`}
    >
      {/* Avatar */}
      <div
        className={`relative flex h-10 w-10 shrink-0 items-center justify-center rounded-2xl font-bold shadow-md transition-transform hover:scale-105 ${
          isBot
            ? 'bg-gradient-to-br from-teal-600 to-teal-800 text-white ring-2 ring-teal-100'
            : 'bg-gradient-to-br from-amber-400 to-amber-600 text-slate-950 ring-2 ring-amber-100'
        }`}
      >
        {isBot ? <Bot className="h-5 w-5 text-teal-100" /> : <User className="h-5 w-5 text-slate-900" />}
        {isBot && (
          <span className="absolute -bottom-0.5 -right-0.5 h-3 w-3 rounded-full bg-emerald-500 ring-2 ring-white"></span>
        )}
      </div>

      {/* Bubble Container */}
      <div className="flex flex-col gap-2 w-full max-w-xl">
        <div
          className={`p-5 rounded-3xl text-sm leading-relaxed shadow-sm transition-all ${
            isBot
              ? 'bg-white border border-slate-200/80 text-slate-800 rounded-tl-sm'
              : 'bg-gradient-to-r from-slate-900 via-slate-800 to-slate-900 text-white rounded-tr-sm shadow-md'
          }`}
        >
          {!isBot && (
            <div className="flex items-center gap-1.5 text-[11px] font-semibold tracking-wider text-amber-300 uppercase mb-2">
              <Sparkles className="h-3 w-3" />
              <span>Transcribed Speech Response</span>
            </div>
          )}

          {isEditing ? (
            <div className="flex flex-col gap-2.5">
              <textarea
                value={editText}
                onChange={(e) => setEditText(e.target.value)}
                className="w-full p-3 rounded-xl border border-slate-300 text-slate-900 text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                rows={2}
              />
              <div className="flex justify-end gap-2">
                <Button variant="ghost" size="sm" onClick={() => setIsEditing(false)}>
                  Cancel
                </Button>
                <Button variant="default" size="sm" onClick={handleSaveEdit} className="bg-teal-700 hover:bg-teal-800">
                  Save Changes
                </Button>
              </div>
            </div>
          ) : (
            <div className="whitespace-pre-wrap font-sans text-sm">{message.text}</div>
          )}

          {/* Footer Timestamp & Audio Listen button */}
          <div
            className={`flex items-center justify-between mt-3 pt-2 border-t text-[11px] ${
              isBot ? 'border-slate-100 text-slate-400' : 'border-slate-700 text-slate-300'
            }`}
          >
            <span>{message.timestamp}</span>
            {isBot && onPlayAudio && (
              <button
                onClick={() => onPlayAudio(message.text)}
                className="inline-flex items-center gap-1.5 font-semibold text-teal-700 hover:text-teal-900 transition-colors bg-teal-50 hover:bg-teal-100 px-2.5 py-1 rounded-lg"
                title="Play Bhashini Audio"
              >
                <Volume2 className="h-3.5 w-3.5" />
                <span>Listen Audio (भाषिणी)</span>
              </button>
            )}
          </div>
        </div>

        {/* Confirmation Action for User Voice Responses */}
        {!isBot && !message.isConfirmed && !isEditing && (
          <div className="flex items-center justify-between gap-3 p-2.5 px-3.5 rounded-2xl bg-amber-50 border border-amber-200/80 text-xs text-amber-950 shadow-sm">
            <span className="font-medium text-[11px]">Verify transcribed input:</span>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setIsEditing(true)}
                className="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg bg-white border border-amber-300 hover:bg-amber-100 font-semibold text-amber-900 transition-colors"
              >
                <Edit2 className="h-3 w-3" />
                Edit
              </button>
              <button
                onClick={() => onConfirm && onConfirm(message.id)}
                className="inline-flex items-center gap-1 px-3 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-700 text-white font-semibold shadow-sm transition-colors"
              >
                <Check className="h-3 w-3" />
                Confirm
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
