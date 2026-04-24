"use client";

import { useState, useEffect, useRef } from "react";
import Link from "next/link";
import { motion } from "framer-motion";

interface Tool {
  name: string;
  description: string;
}

interface CommandResponse {
  success: boolean;
  message: string;
  data?: any;
}

interface ChatMessage {
  id: number;
  role: "user" | "assistant";
  content: string;
  timestamp: Date;
}

export default function Dashboard() {
  const [tools, setTools] = useState<Tool[]>([]);
  const [selectedTool, setSelectedTool] = useState<string>("");
  const [response, setResponse] = useState<CommandResponse | null>(null);
  const [loading, setLoading] = useState<boolean>(false);
  const [parameters, setParameters] = useState<string>("{}");
  
  // Chat interface
  const [chatMessages, setChatMessages] = useState<ChatMessage[]>([]);
  const [chatInput, setChatInput] = useState<string>("");
  const [chatLoading, setChatLoading] = useState<boolean>(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  // Feature tree and BOM state
  const [featureTree, setFeatureTree] = useState<any[]>([]);
  const [bomData, setBomData] = useState<any>(null);

  useEffect(() => {
    // Mock fetch of tools
    const mockTools: Tool[] = [
      { name: "nx_create_plate", description: "Create a rectangular plate" },
      { name: "nx_create_bracket", description: "Create an L-shaped bracket" },
      { name: "nx_create_flange", description: "Create a circular flange" },
      { name: "nx_create_boss", description: "Create a boss feature" },
      { name: "nx_create_hole_pattern", description: "Create a pattern of holes" },
      { name: "nx_list_features", description: "List all features" },
      { name: "nx_list_components", description: "List assembly components" },
      { name: "nx_generate_bom", description: "Generate Bill of Materials" },
      { name: "nx_ai_review_engine", description: "Run AI design review" },
      { name: "nx_prepare_for_manufacturing", description: "Prepare for manufacturing" },
    ];
    setTools(mockTools);
  }, []);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages]);

  const handleRunCommand = async () => {
    setLoading(true);
    setResponse(null);
    try {
      const params = JSON.parse(parameters);
      // Mock response
      setResponse({
        success: true,
        message: `Executed ${selectedTool} successfully!`,
        data: { ...params, tool: selectedTool, timestamp: new Date().toISOString() },
      });
    } catch (err) {
      setResponse({
        success: false,
        message: "Failed to execute command",
        data: { error: String(err) },
      });
    } finally {
      setLoading(false);
    }
  };

  const handleSendChat = async () => {
    if (!chatInput.trim()) return;
    const userMessage: ChatMessage = {
      id: Date.now(),
      role: "user",
      content: chatInput,
      timestamp: new Date(),
    };
    setChatMessages((prev) => [...prev, userMessage]);
    const input = chatInput;
    setChatInput("");
    setChatLoading(true);
    
    // Mock AI response
    setTimeout(() => {
      const aiMessage: ChatMessage = {
        id: Date.now() + 1,
        role: "assistant",
        content: `I understand you want to: "${input}".\n\nI can help you with that using NXPilot AI tools. For example, if you want to create a part, I can use nx_create_plate, nx_create_bracket, or other intelligent modeling tools.`,
        timestamp: new Date(),
      };
      setChatMessages((prev) => [...prev, aiMessage]);
      setChatLoading(false);
    }, 1000);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-indigo-50 font-sans">
      {/* Header */}
      <nav className="bg-white/80 backdrop-blur-md border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <Link href="/" className="flex items-center gap-2">
                <div className="w-10 h-10 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl flex items-center justify-center text-white font-bold text-xl">
                  NX
                </div>
                <span className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
                  Pilot AI
                </span>
              </Link>
            </div>
            <div className="flex items-center gap-6">
              <Link href="/" className="text-gray-600 hover:text-blue-600 font-medium transition-colors">
                Home
              </Link>
            </div>
          </div>
        </div>
      </nav>

      <div className="max-w-7xl mx-auto p-6">
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-2">NXPilot AI Dashboard</h1>
          <p className="text-gray-600">Connect and control Siemens NX from your browser</p>
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Left Column - Feature Tree & BOM */}
          <div className="lg:col-span-1 space-y-6">
            {/* Feature Tree */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-2xl shadow-xl p-6"
            >
              <h3 className="text-xl font-bold text-gray-900 mb-4">Feature Tree</h3>
              <div className="bg-gray-50 rounded-xl p-4 min-h-[200px] max-h-[300px] overflow-y-auto">
                <ul className="space-y-2">
                  <li className="text-sm text-gray-700 pl-4 border-l-2 border-blue-500">
                    Base Feature (Extrude)
                  </li>
                  <li className="text-sm text-gray-700 pl-8 border-l-2 border-indigo-400">
                    Hole Pattern (4x M8)
                  </li>
                  <li className="text-sm text-gray-700 pl-8 border-l-2 border-indigo-400">
                    Fillets (R2mm)
                  </li>
                </ul>
                <button
                  onClick={() => setFeatureTree([{ name: "Mock Feature 1" }, { name: "Mock Feature 2" }])}
                  className="mt-4 text-blue-600 hover:text-blue-700 text-sm font-medium"
                >
                  Refresh Features
                </button>
              </div>
            </motion.div>

            {/* BOM */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.1 }}
              className="bg-white rounded-2xl shadow-xl p-6"
            >
              <h3 className="text-xl font-bold text-gray-900 mb-4">Bill of Materials</h3>
              <div className="bg-gray-50 rounded-xl p-4">
                {bomData ? (
                  <pre className="text-sm font-mono">{JSON.stringify(bomData, null, 2)}</pre>
                ) : (
                  <p className="text-gray-500 text-sm">No BOM generated yet</p>
                )}
                <button
                  onClick={() => setBomData({
                    items: [
                      { name: "Base Plate", qty: 1, material: "Aluminum 6061" },
                      { name: "Bracket Arm", qty: 1, material: "Aluminum 6061" },
                    ]
                  })}
                  className="mt-4 w-full bg-gradient-to-r from-indigo-500 to-purple-500 text-white py-2 rounded-xl font-semibold hover:shadow-lg transition-all"
                >
                  Generate BOM
                </button>
              </div>
            </motion.div>
          </div>

          {/* Middle Column - Model Preview & Tool Execution */}
          <div className="lg:col-span-1 space-y-6">
            {/* Model Preview */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.2 }}
              className="bg-white rounded-2xl shadow-xl p-6"
            >
              <h3 className="text-xl font-bold text-gray-900 mb-4">Model Preview</h3>
              <div className="bg-gradient-to-br from-gray-100 to-gray-200 rounded-xl aspect-video flex items-center justify-center">
                <div className="text-center">
                  <div className="w-16 h-16 bg-gradient-to-r from-blue-600 to-indigo-600 rounded-2xl mx-auto mb-4 flex items-center justify-center">
                    <div className="w-8 h-8 bg-white rounded-lg"></div>
                  </div>
                  <p className="text-gray-600 font-medium">3D Preview</p>
                  <p className="text-sm text-gray-400">Connect to NX for real model</p>
                </div>
              </div>
            </motion.div>

            {/* Tool Execution */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.3 }}
              className="bg-white rounded-2xl shadow-xl p-6"
            >
              <h3 className="text-xl font-bold text-gray-900 mb-4">Execute Tool</h3>
              <div className="mb-4">
                <label className="block text-sm font-semibold text-gray-700 mb-2">Select Tool</label>
                <select
                  className="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                  value={selectedTool}
                  onChange={(e) => setSelectedTool(e.target.value)}
                >
                  <option value="">Choose a tool...</option>
                  {tools.map((tool) => (
                    <option key={tool.name} value={tool.name}>
                      {tool.name}
                    </option>
                  ))}
                </select>
                {selectedTool && (
                  <p className="text-sm text-gray-500 mt-2">
                    {tools.find((t) => t.name === selectedTool)?.description}
                  </p>
                )}
              </div>
              <div className="mb-4">
                <label className="block text-sm font-semibold text-gray-700 mb-2">Parameters (JSON)</label>
                <textarea
                  className="w-full p-3 border border-gray-300 rounded-xl h-24 font-mono text-sm"
                  value={parameters}
                  onChange={(e) => setParameters(e.target.value)}
                  placeholder='{"length": 100, "width": 50, "thickness": 20}'
                />
              </div>
              <button
                onClick={handleRunCommand}
                disabled={loading || !selectedTool}
                className="w-full bg-gradient-to-r from-blue-600 to-indigo-600 text-white py-3 rounded-xl font-semibold hover:shadow-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all"
              >
                {loading ? "Running..." : "Run Command"}
              </button>
            </motion.div>
          </div>

          {/* Right Column - Chat Interface & Response */}
          <div className="lg:col-span-1 space-y-6">
            
            {/* Chat Interface */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
              className="bg-white rounded-2xl shadow-xl p-6 flex flex-col"
              style={{ height: "calc(100vh - 250px)" }}
            >
              <h3 className="text-xl font-bold text-gray-900 mb-4">AI Copilot Chat</h3>
              
              {/* Chat messages */}
              <div className="flex-1 bg-gray-50 rounded-xl p-4 overflow-y-auto mb-4 space-y-4">
                {chatMessages.length === 0 && (
                  <div className="text-center text-gray-500 py-8">
                    <p>Ask me anything about your CAD model!</p>
                    <p className="text-sm mt-2">e.g., "Create a 100x50x20mm plate"</p>
                  </div>
                )}
                {chatMessages.map((msg) => (
                  <div
                    key={msg.id}
                    className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                  >
                    <div
                      className={`max-w-[80%] p-4 rounded-2xl ${
                        msg.role === "user"
                          ? "bg-gradient-to-r from-blue-600 to-indigo-600 text-white"
                          : "bg-white border border-gray-200 text-gray-800"
                      }`}
                    >
                      <p className="whitespace-pre-wrap">{msg.content}</p>
                      <p className="text-xs opacity-70 mt-2">
                        {msg.timestamp.toLocaleTimeString()}
                      </p>
                    </div>
                  </div>
                ))}
                {chatLoading && (
                  <div className="flex justify-start">
                    <div className="bg-white border border-gray-200 text-gray-800 p-4 rounded-2xl">
                      <p className="animate-pulse">Thinking...</p>
                    </div>
                  </div>
                )}
                <div ref={chatEndRef} />
              </div>

              {/* Chat input */}
              <div className="flex gap-2">
                <input
                  type="text"
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleSendChat()}
                  placeholder="Ask AI to help with your CAD model..."
                  className="flex-1 p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                />
                <button
                  onClick={handleSendChat}
                  disabled={chatLoading}
                  className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-6 py-3 rounded-xl font-semibold hover:shadow-lg disabled:opacity-50 transition-all"
                >
                  Send
                </button>
              </div>
            </motion.div>

            {/* Command Response */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.5 }}
              className="bg-white rounded-2xl shadow-xl p-6"
            >
              <h3 className="text-xl font-bold text-gray-900 mb-4">Tool Response</h3>
              {response ? (
                <div className="p-4 rounded-xl bg-gray-50">
                  <div
                    className={`inline-block px-3 py-1 rounded-full text-sm font-semibold mb-4 ${
                      response.success ? "bg-green-100 text-green-800" : "bg-red-100 text-red-800"
                    }`}
                  >
                    {response.success ? "Success" : "Error"}
                  </div>
                  <p className="text-gray-700 mb-4">{response.message}</p>
                  {response.data && (
                    <pre className="bg-gray-100 p-4 rounded-lg font-mono text-sm overflow-auto max-h-40">
                      {JSON.stringify(response.data, null, 2)}
                    </pre>
                  )}
                </div>
              ) : (
                <div className="text-center text-gray-500 py-8">
                  <p>No command executed yet</p>
                </div>
              )}
            </motion.div>
          </div>
        </div>
      </div>
    </div>
  );
}
