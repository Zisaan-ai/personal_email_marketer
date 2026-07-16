
@app.post("/api/run-warmup")
def trigger_warmup_manual(current_user: database.User = Depends(get_current_user)):
    """Manually trigger a warmup cycle for testing."""
    import warmup_service
    import threading
    threading.Thread(target=warmup_service.run_warmup_cycle).start()
    return {"status": "success", "message": "Warmup cycle triggered in background"}
