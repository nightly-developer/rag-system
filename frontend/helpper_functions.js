export function formatConvHistory(messages) {
  return messages.map((message, i) => {
    if (i % 2 === 0) {
      return `Human: ${message}`
    } else {
      return `AI: ${message}`
    }
  }).join('\n')
}

export function combineDocuments(docs) {
  return docs.map((doc) => doc.pageContent).join('\n\n')
}