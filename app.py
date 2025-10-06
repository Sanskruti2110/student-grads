from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# In-memory storage for student records
students = {}

# Binary search helper
def binary_search(arr, target):
    low, high = 0, len(arr) - 1
    while low <= high:
        mid = (low + high) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_student():
    data = request.json
    roll = str(data["roll"])
    name = data["name"]
    subjects = data["subjects"]
    total = sum(subjects)

    students[roll] = {"name": name, "subjects": subjects, "total": total}
    return jsonify({"message": f"Record added for Roll No {roll}!"})

@app.route("/update", methods=["POST"])
def update_student():
    data = request.json
    roll = str(data["roll"])
    if roll not in students:
        return jsonify({"message": f"Record not found for Roll No {roll}!"}), 404

    students[roll]["name"] = data["name"]
    students[roll]["subjects"] = data["subjects"]
    students[roll]["total"] = sum(data["subjects"])
    return jsonify({"message": f"Record updated for Roll No {roll}!"})

@app.route("/delete", methods=["POST"])
def delete_student():
    data = request.json
    roll = str(data["roll"])
    if roll in students:
        del students[roll]
        return jsonify({"message": f"Record deleted for Roll No {roll}!"})
    return jsonify({"message": f"No record found for Roll No {roll}!"}), 404

@app.route("/view/<roll>", methods=["GET"])
def view_student(roll):
    roll = str(roll)
    sorted_rolls = sorted(students.keys())
    idx = binary_search(sorted_rolls, roll)

    if idx == -1:
        return jsonify({"message": "Record not found", "record": None}), 404

    student = students[sorted_rolls[idx]]
    return jsonify({"message": "Record found", "record": student})

@app.route("/view_all", methods=["GET"])
def view_all_students():
    return jsonify({"records": students})

if __name__ == "__main__":
    app.run(debug=True)
