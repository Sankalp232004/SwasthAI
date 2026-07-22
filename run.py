"""
SwasthAI Application Entry Point
Run: python run.py
"""
import os
from app import create_app

env = os.environ.get('FLASK_ENV', 'development')
app = create_app('production' if env == 'production' else 'development')


if __name__ == '__main__':
    print("\n" + "="*50)
    print("  SwasthAI - Medical Triage System")
    print("="*50)
    print("\n  Patient Portal:  http://127.0.0.1:5000/")
    print("  Doctor Portal:   http://127.0.0.1:5000/doctor/login")
    print("="*50 + "\n")

    # Bind to 0.0.0.0 for Docker container access
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', os.environ.get('FLASK_PORT', 5000)))
    debug = env == 'development'

    app.run(host=host, port=port, debug=debug, threaded=True)
