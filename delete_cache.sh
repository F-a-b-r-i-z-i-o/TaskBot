#!/bin/bash
find . -name "*.pyc" -delete
find . -name "__pycache__" -delete
find . -name "*.pytest_cache" -exec rm -rf {} +