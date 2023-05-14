namespace py Test

typedef i32 ResultCode

service ConfigService {
    ConfigResponse get_config(1:ConfigRequest request)
}

struct ConfigRequest {
    1:string hostname
    2:string username
    3:string password
    4:string input_file
}

struct ConfigResponse {
    1:bool success
    2:string message
}
