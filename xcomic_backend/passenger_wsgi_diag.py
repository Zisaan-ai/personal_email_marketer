import sys
import os
import time
import traceback

def application(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    
    output = []
    output.append("=== Python Diagnostics starting ===")
    output.append(f"Python Version: {sys.version}")
    output.append(f"CWD: {os.getcwd()}")
    output.append(f"PATH: {sys.path}")
    
    # Measure import main time
    t0 = time.time()
    try:
        output.append("\nAttempting to import main...")
        import main
        output.append(f"Import main successful in {time.time() - t0:.4f} seconds!")
        
        # Test database session
        t1 = time.time()
        output.append("\nAttempting database query...")
        db = main.database.SessionLocal()
        users = db.query(main.database.User).all()
        output.append(f"Database query successful in {time.time() - t1:.4f} seconds! Users count: {len(users)}")
        db.close()
        
    except Exception as e:
        output.append(f"\nImport/Query failed: {e}")
        output.append(traceback.format_exc())
        
    return ["\n".join(output).encode('utf-8')]
