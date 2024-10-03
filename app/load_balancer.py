FILE_MICROSSERVICES = ["https://pdist-file-service.onrender.com/api/files/", "https://pdist-file-service-1.onrender.com/api/files/"]
POST_MICROSSERVICES = ["http://localhost:8082/api/posts"]
FORUM_MICROSSERVICES = ["https://pdist-back-1.onrender.com/api/forums/","https://pdist-back.onrender.com/api/forums/"]
COMMENT_MICROSSERVICES = ["https://pdist-back-1.onrender.com/api/comments/","https://pdist-back.onrender.com/api/comments/"]

round_robin_counters = {
    "files": 0,
    "posts": 0,
    "comments": 0,
    "forums": 0,
}

current_instance = 0

def get_next_instance(service_name):
    """Retorna a próxima instância de serviço usando round robin."""
    global round_robin_counters
    if service_name == "files":
        instance = FILE_MICROSSERVICES[round_robin_counters[service_name] % len(FILE_MICROSSERVICES)]
    elif service_name == "posts":
        instance = POST_MICROSSERVICES[round_robin_counters[service_name] % len(POST_MICROSSERVICES)]
    elif service_name == "comments":
        instance = COMMENT_MICROSSERVICES[round_robin_counters[service_name] % len(COMMENT_MICROSSERVICES)]
    elif service_name == "forums":
        instance = FORUM_MICROSSERVICES[round_robin_counters[service_name] % len(FORUM_MICROSSERVICES)]
    else:
        raise HTTPException(status_code=404, detail="Serviço não encontrado")
    
    round_robin_counters[service_name] += 1
    return instance