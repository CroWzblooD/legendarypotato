'use client';

import { useState } from 'react';
import ChatContainer from '@/components/chat/ChatContainer';
import ProfileSidebar from '@/components/student/ProfileSidebar';
import { UserInfo, ChatMessage } from '@/lib/types';

export default function Home() {
  const [currentUser, setCurrentUser] = useState<UserInfo>({
    user_id: 'demo-user',
    name: 'Demo Student',
    grade_level: '10',
    learning_style_summary: 'Visual learner, prefers structured notes with examples',
    emotional_state_summary: 'Focused and motivated to learn',
    mastery_level_summary: 'Level 6: Good understanding, ready for application',
    teaching_style: 'direct'
  });

  const [chatHistory, setChatHistory] = useState<ChatMessage[]>([]);
  const [conversationId, setConversationId] = useState<string | undefined>();

  const handleUserUpdate = (updatedUser: UserInfo) => {
    setCurrentUser(updatedUser);
  };

  const handleNewMessage = (message: ChatMessage) => {
    setChatHistory(prev => [...prev, message]);
  };

  const handleConversationIdUpdate = (id: string) => {
    setConversationId(id);
  };

  return (
    <main className="flex h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Sidebar */}
      <ProfileSidebar 
        userInfo={currentUser} 
        onUserUpdate={handleUserUpdate}
      />

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <header className="bg-white border-b border-gray-200 px-6 py-4 shadow-sm">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                AI Tutor Orchestrator
              </h1>
              <p className="text-sm text-gray-600">
                Intelligent educational tool orchestration
              </p>
            </div>
            <div className="flex items-center gap-4">
              <div className="text-right">
                <p className="text-sm font-medium text-gray-900">
                  {currentUser.name}
                </p>
                <p className="text-xs text-gray-500">
                  Grade {currentUser.grade_level}
                </p>
              </div>
              <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-indigo-600 rounded-full flex items-center justify-center text-white font-semibold">
                {currentUser.name.charAt(0)}
              </div>
            </div>
          </div>
        </header>

        {/* Chat Container */}
        <ChatContainer
          userInfo={currentUser}
          chatHistory={chatHistory}
          conversationId={conversationId}
          onNewMessage={handleNewMessage}
          onConversationIdUpdate={handleConversationIdUpdate}
        />
      </div>
    </main>
  );
}
