from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_documents(file_data,chunk_size=500,chunk_overlap=50):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap,
        separators=["\n\n","\n"," ",""]
    )

    chunks = []
    for file in file_data:
        splits = text_splitter.split_text(file["content"])
        for item, chunk in enumerate(splits):
            chunks.append({
                "text":chunk,
                "metadata":{
                    "source":file["path"],
                    "chunk_id":item
                }
            })
    return chunks