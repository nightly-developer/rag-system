import { PromptTemplate } from "@langchain/core/prompts"
import { StringOutputParser } from "@langchain/core/output_parsers";
import { RunnablePassthrough, RunnableSequence } from "@langchain/core/runnables"

import { retriever } from "./retriever";
import { combineDocuments, formatConvHistory } from "./helpper_functions";

// =============================Open AI========================================
// import { ChatOpenAI } from "langchain/chat_models/openai"
// const openAIApiKey = process.env.OPENAI_API_KEY
// import { OpenAIEmbeddings } from "langchain/embeddings/openai"
// const embeddings = new OpenAIEmbeddings({ openAIApiKey })
// const llm = new ChatOpenAI({ openAIApiKey })
// =============================Gemini=========================================
import { ChatGoogleGenerativeAI } from "@langchain/google-genai";
const googleApiKey = import.meta.env.VITE_GOOGLE_API_KEY // process.env.GOOGLE_API_KEY
// import { GoogleGenerativeAIEmbeddings } from "@langchain/google-genai";
// const embeddings = new GoogleGenerativeAIEmbeddings({ apiKey: googleApiKey })
const llm = new ChatGoogleGenerativeAI({ apiKey: googleApiKey })
// ============================================================================

document.addEventListener('submit', (e) => {
  e.preventDefault()
  progressConversation()
})
const standaloneQuestionTemplate = `Given some conversation history (if any) and a question, convert the question to a standalone question. 
conversation history: {conv_history}
question: {question} 
standalone question:`
const standaloneQuestionPrompt = PromptTemplate.fromTemplate(standaloneQuestionTemplate)

const answerTemplate = `You are a helpful and enthusiastic support bot who can answer a given question about Weka, a GUI tool use for machine learning based on the context provided and the conversation history. Try to find the answer in the context. If the answer is not given in the context, find the answer in the conversation history if possible. If you really don't know the answer, say "I'm sorry, I don't know the answer to that. Don't try to make up an answer. Always speak as if you were chatting to a friend.
context: {context}
conversation history: {conv_history}
question: {question}
answer: `

const answerPrompt = PromptTemplate.fromTemplate(answerTemplate)

const standaloneQuestionChain = standaloneQuestionPrompt
  .pipe(llm)
  .pipe(new StringOutputParser())

const retrieverChain = RunnableSequence.from([
  prevResult => prevResult.standalone_question,
  retriever,
  combineDocuments
])
const answerChain = answerPrompt
  .pipe(llm)
  .pipe(new StringOutputParser())

const chain = RunnableSequence.from([
  {
    standalone_question: standaloneQuestionChain,
    original_input: new RunnablePassthrough()
  },
  {
    context: retrieverChain,
    question: ({ original_input }) => original_input.question,
    conv_history: ({ original_input }) => original_input.conv_history
  },
  answerChain
])

const convHistory = []

async function progressConversation() {
  const userInput = document.getElementById('user-input')
  const chatbotConversation = document.getElementById('chatbot-conversation-container')
  const question = userInput.value
  userInput.value = ''

  // add human message
  const newHumanSpeechBubble = document.createElement('div')
  newHumanSpeechBubble.classList.add('speech', 'speech-human')
  chatbotConversation.appendChild(newHumanSpeechBubble)
  newHumanSpeechBubble.textContent = question
  chatbotConversation.scrollTop = chatbotConversation.scrollHeight
  const response = await chain.invoke({
    question: question,
    conv_history: formatConvHistory(convHistory)
  })
  convHistory.push(question)
  convHistory.push(response)

  // add AI message
  const newAiSpeechBubble = document.createElement('div')
  newAiSpeechBubble.classList.add('speech', 'speech-ai')
  chatbotConversation.appendChild(newAiSpeechBubble)
  newAiSpeechBubble.textContent = response
  chatbotConversation.scrollTop = chatbotConversation.scrollHeight
}