from app import app,db
from flask import jsonify,request
from models import User
from werkzeug.exceptions import BadRequest,NotFound
from flask_jwt_extended import get_jwt_identity,jwt_required
from flask_migrate import Migrate
from components.repo_loader import clone_repo, load_repo_files
from components.chunker import chunk_documents
from components.rag_pipeline import create_vector_store, answer_question, create_qa_chain
from flask_jwt_extended import create_access_token

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    new_user = User(username=username, email=email)
    new_user.set_password(password)  # ✅ Set password securely

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 200




@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid credentials"}), 400  # ✅ JSON error

    access_token = create_access_token(identity=username)
    return jsonify({"access_token": access_token}), 200




@app.route('/process_repo', methods=['POST'])
# @jwt_required()
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
# @jwt_required()
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
