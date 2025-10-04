'use client';

import { ChatMessage } from '@/lib/types';
import { formatTimestamp } from '@/lib/utils';
import NoteMakerRenderer from '../tools/NoteMakerRenderer';
import FlashcardRenderer from '../tools/FlashcardRenderer';
import ConceptExplainerRenderer from '../tools/ConceptExplainerRenderer';

interface MessageListProps {
  messages: Array<ChatMessage & { toolResponse?: any; extractedParams?: any }>;
}

export default function MessageList({ messages }: MessageListProps) {
  return (
    <div className="space-y-6">
      {messages.map((message, index) => (
        <div
          key={index}
          className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
        >
          <div
            className={`max-w-3xl ${
              message.role === 'user'
                ? 'bg-gradient-to-r from-blue-500 to-indigo-600 text-white'
                : 'bg-gray-100 text-gray-900'
            } rounded-2xl px-6 py-4 shadow-sm`}
          >
            {/* Message Header */}
            <div className="flex items-center gap-2 mb-2">
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center text-sm font-semibold ${
                  message.role === 'user'
                    ? 'bg-white/20 text-white'
                    : 'bg-gradient-to-br from-purple-500 to-pink-500 text-white'
                }`}
              >
                {message.role === 'user' ? 'U' : 'AI'}
              </div>
              <div>
                <p className={`text-sm font-medium ${message.role === 'user' ? 'text-white' : 'text-gray-900'}`}>
                  {message.role === 'user' ? 'You' : 'AI Tutor'}
                </p>
                {message.timestamp && (
                  <p className={`text-xs ${message.role === 'user' ? 'text-white/70' : 'text-gray-500'}`}>
                    {formatTimestamp(message.timestamp)}
                  </p>
                )}
              </div>
            </div>

            {/* Message Content */}
            <div className="prose prose-sm max-w-none">
              <p className={message.role === 'user' ? 'text-white' : 'text-gray-800'}>
                {message.content}
              </p>
            </div>

            {/* Extracted Parameters Display (for debugging/demo) */}
            {message.extractedParams && message.role === 'assistant' && (
              <div className="mt-3 pt-3 border-t border-gray-200">
                <details className="text-sm">
                  <summary className="cursor-pointer text-gray-600 font-medium hover:text-gray-900">
                    🔍 Parameter Extraction Details
                  </summary>
                  <div className="mt-2 space-y-1 text-xs">
                    <p>
                      <span className="font-semibold">Tool:</span>{' '}
                      <span className="bg-blue-100 text-blue-800 px-2 py-0.5 rounded">
                        {message.extractedParams.tool_type}
                      </span>
                    </p>
                    <p>
                      <span className="font-semibold">Confidence:</span>{' '}
                      <span className="bg-green-100 text-green-800 px-2 py-0.5 rounded">
                        {(message.extractedParams.confidence * 100).toFixed(0)}%
                      </span>
                    </p>
                    {Object.keys(message.extractedParams.inferred_params || {}).length > 0 && (
                      <div>
                        <span className="font-semibold">Inferred:</span>
                        <ul className="list-disc list-inside ml-2 text-gray-600">
                          {Object.entries(message.extractedParams.inferred_params).map(([key, value]) => (
                            <li key={key}>
                              {key}: <span className="font-mono">{String(value)}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    )}
                  </div>
                </details>
              </div>
            )}

            {/* Tool Response */}
            {message.toolResponse && message.toolResponse.success && (
              <div className="mt-4">
                {message.toolResponse.tool_type === 'note_maker' && (
                  <NoteMakerRenderer data={message.toolResponse.data} />
                )}
                {message.toolResponse.tool_type === 'flashcard_generator' && (
                  <FlashcardRenderer data={message.toolResponse.data} />
                )}
                {message.toolResponse.tool_type === 'concept_explainer' && (
                  <ConceptExplainerRenderer data={message.toolResponse.data} />
                )}
              </div>
            )}

            {/* Tool Error */}
            {message.toolResponse && !message.toolResponse.success && (
              <div className="mt-4 bg-red-50 border border-red-200 rounded-lg p-3">
                <p className="text-sm text-red-700 font-medium">⚠️ Tool Error</p>
                <p className="text-xs text-red-600 mt-1">{message.toolResponse.error}</p>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}
