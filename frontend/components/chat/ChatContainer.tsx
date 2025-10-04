'use client';

import { useState, useRef, useEffect } from 'react';
import { UserInfo, ChatMessage, ChatResponse } from '@/lib/types';
import { apiClient } from '@/lib/api';
import MessageList from './MessageList';
import MessageInput from './MessageInput';
import TypingIndicator from './TypingIndicator';

interface ChatContainerProps {
  userInfo: UserInfo;
  chatHistory: ChatMessage[];
  conversationId?: string;
  onNewMessage: (message: ChatMessage) => void;
  onConversationIdUpdate: (id: string) => void;
}

export default function ChatContainer({
  userInfo,
  chatHistory,
  conversationId,
  onNewMessage,
  onConversationIdUpdate,
}: ChatContainerProps) {
  const [messages, setMessages] = useState<Array<ChatMessage & { toolResponse?: any; extractedParams?: any }>>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return;

    // Add user message immediately
    const userMessage: ChatMessage = {
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };

    setMessages(prev => [...prev, userMessage]);
    onNewMessage(userMessage);
    setIsLoading(true);
    setError(null);

    try {
      // Call orchestrator API
      const response: ChatResponse = await apiClient.chat({
        message: content,
        user_info: userInfo,
        conversation_id: conversationId,
        chat_history: chatHistory,
      });

      // Update conversation ID
      if (response.conversation_id && response.conversation_id !== conversationId) {
        onConversationIdUpdate(response.conversation_id);
      }

      // Add assistant response
      const assistantMessage = {
        role: 'assistant' as const,
        content: response.message,
        timestamp: new Date().toISOString(),
        toolResponse: response.tool_response,
        extractedParams: response.extracted_parameters,
      };

      setMessages(prev => [...prev, assistantMessage]);
      onNewMessage(assistantMessage);

    } catch (err: any) {
      console.error('Error sending message:', err);
      setError(err.message || 'Failed to send message. Please try again.');
      
      // Add error message
      setMessages(prev => [...prev, {
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex-1 flex flex-col bg-white">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full">
            <div className="text-center max-w-md">
              <div className="w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center mx-auto mb-4">
                <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                </svg>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">
                Welcome to AI Tutor!
              </h3>
              <p className="text-gray-600">
                Ask me to create notes, generate flashcards, or explain concepts. 
                I'll intelligently orchestrate the right educational tools for you.
              </p>
              <div className="mt-6 text-left space-y-2 text-sm text-gray-500">
                <p>💡 Try asking:</p>
                <ul className="list-disc list-inside space-y-1">
                  <li>"Create notes on photosynthesis"</li>
                  <li>"I'm struggling with derivatives, need practice"</li>
                  <li>"Explain how mitochondria work"</li>
                </ul>
              </div>
            </div>
          </div>
        ) : (
          <MessageList messages={messages} />
        )}
        
        {isLoading && <TypingIndicator />}
        
        {error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
            <p className="font-medium">Error</p>
            <p className="text-sm">{error}</p>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <MessageInput 
        onSendMessage={handleSendMessage} 
        disabled={isLoading}
      />
    </div>
  );
}
