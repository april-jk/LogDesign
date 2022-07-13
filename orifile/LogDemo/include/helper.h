#pragma once

#define RET_SUCCESS          0
#define RET_ERROR_FILEID -1
#define RET_ERROR_EID     -2

#define DLL_EXPORT           __declspec(dllexport)

//文件信息结构体
struct LogFilesInfo{
    char szFileName[256];
    int  nEventCount;
};

//事件信息结构体
struct EventInfo {
    char szTime[64];
    char szEventID[32];
    char szEventLevel[32];
    char szComputerName[128];
    char szSourceName[128];
    char szStrings[4096];
};

//初始化函数
DLL_EXPORT bool Init();

//加载日志文件，参数为日志文件路径
DLL_EXPORT bool LoadLogFile(const char *logPath);

//加载日志文件，参数为日志文件所在文件夹路径
DLL_EXPORT bool LoadLogFolder(const char *logPath);

//获取日志文件数量
DLL_EXPORT int GetLogFileCount();

//获取指定文件的文件名称
DLL_EXPORT const char *GetLogFileName(int fileId);

//获取指定文件的事件总数
DLL_EXPORT int GetLogFileEventCount(int fileId);

//获取指定文件的某条事件
DLL_EXPORT int GetLogFileEvent(int fileId, int eId, EventInfo *lpEvent);

//释放所加载的日志文件
DLL_EXPORT void Release();
