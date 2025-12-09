#!/bin/bash
echo "Building LX Multi Capture Frontend..."
cd frontend
npm run build
cd ..
echo "Build complete! Frontend files are in frontend/dist/"

