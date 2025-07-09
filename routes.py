from app import app,db
from flask import jsonify,request
from models import User
from werkzeug.exceptions import BadRequest,NotFound
from flask_jwt_extended import get_jwt_identity,jwt_required
from flask_migrate import Migrate
from components.repo_loader import clone_repo, load_repo_files
from components.chunker import chunk_documents
from components.rag_pipeline import create_vector_store, answer_question, create_qa_chain


@app.route('/register',methods=['POST'])
def register_user():
    data = request.get_json()
    if not data:
        return {"message":"Invalid Data"},400
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    if not email or not username or not password:
        return {"message":"Invalid Data"},400
    user = User(email=email,username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify(message="User registered successfully"),201


@app.route('/login',methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        raise BadRequest("Invalid data")
    email = data.get("email")
    password = data.get("password")
    token,_ = User.authenticate(email,password)
    if not token:
        raise BadRequest("Invalid Credentials")
    return jsonify(access_token=token),200



@app.route('/process_repo', methods=['POST'])
def process_repo():
    try:
        repo_url = request.json.get("repo_url")
        if not repo_url:
            return jsonify({"error": "Missing repo_url"}), 400

        clone_dir = clone_repo(repo_url)
        if not clone_dir:
            return jsonify({"error": "Failed to clone repo"}), 500

        files_data = load_repo_files(clone_dir)
        if not files_data:
            return jsonify({"error": "No supported files found in repo."}), 400

        chunks = chunk_documents(files_data)
        if not chunks:
            return jsonify({"error": "Failed to generate chunks."}), 500

        create_vector_store(chunks)

        return jsonify({"message": "Repo processed and embedded successfully"}), 200

    except Exception as e:
        import traceback
        print("❌ Exception in /process_repo:", e)
        traceback.print_exc()
        return jsonify({"error": "Server error", "details": str(e)}), 500

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question = data.get('question')

    if not question:
        return jsonify({"error": "Question is required"}), 400

    try:
        chain = create_qa_chain()
        result = chain.invoke({"query": question})  # ✅ Correct way for multi-output

        return jsonify({
            "answer": result["result"],
            "sources": [doc.metadata for doc in result.get("source_documents", [])]
        })
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500
