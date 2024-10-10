// import { OpenAIEmbeddings } from 'langchain/embeddings/openai'
import { GoogleGenerativeAIEmbeddings } from "@langchain/google-genai";

import { SupabaseVectorStore } from "@langchain/community/vectorstores/supabase";
import { createClient } from '@supabase/supabase-js'

// const openAIApiKey = process.env.OPENAI_API_KEY
// const embeddings = new OpenAIEmbeddings({ openAIApiKey })

const googleApiKey = import.meta.env.VITE_GOOGLE_API_KEY // process.env.VITE_GOOGLE_API_KEY //
const embeddings = new GoogleGenerativeAIEmbeddings({
  apiKey: googleApiKey,
  model: "text-embedding-004",
})

const sbApiKey = import.meta.env.VITE_SB_API_KEY // process.env.VITE_SB_API_KEY // 
const sbUrl = import.meta.env.VITE_SB_URL // process.env.VITE_SB_URL // 
const supabase = createClient(sbUrl, sbApiKey)

const vectorStore = new SupabaseVectorStore(embeddings, {
  client: supabase,
  table_name: "documents",
  query_name: "match_documents",
  chunk_size: 500
})

const retriever = vectorStore.asRetriever()

export { retriever }