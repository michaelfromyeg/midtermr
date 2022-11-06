curl -X POST -H "Content-Type: application/json" \
    -d '{"name": "test-exam", "filename": ""}' \
    http://localhost:5000/exams

# curl -X POST -F 'image=@/home/user/Pictures/wallpaper.jpg' http://example.com/upload
