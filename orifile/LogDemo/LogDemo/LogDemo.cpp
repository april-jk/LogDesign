// LogDemo.cpp : 此文件包含 "main" 函数。程序执行将在此处开始并结束。
//

#include <iostream>
#include <tchar.h>
#include <atlconv.h>
#include "../include/helper.h"
#pragma comment(lib, "LogHelper.lib")
using namespace std;

void DealFolder(const char* foldPath)
{
    //加载指定文件夹的所有日志
    LoadLogFolder(foldPath);
    int fileCount = GetLogFileCount();
    cout << "file count: " << fileCount << endl;

    //遍历所有文件

    //设置每个文件最大输出条数
    int iMaxOutPut = 3;
    for (auto fileId = 0; fileId < fileCount; ++fileId) {
        const char* fileName = GetLogFileName(fileId);
        if (fileName == NULL) {
            cout << "fileId Error" << endl;
            return;
        }

        const int   fileEventCount = GetLogFileEventCount(fileId);
        if (fileEventCount == RET_ERROR_FILEID) {
            cout << "fileId Error" << endl;
            return;
        }

        cout << "fileName: " << fileName << "\tEventCount: " << fileEventCount << endl;

        const auto eInfo = new EventInfo();
        for (auto eId = 0; eId < fileEventCount; ++eId) {
            int iRet = GetLogFileEvent(fileId, 0, eInfo);
            if (iRet == RET_SUCCESS) {
                cout << "Time: " << eInfo->szTime << endl;
                cout << "EventID: " << eInfo->szEventID << endl;
                cout << "EventLevel: " << eInfo->szEventLevel << endl;
                cout << "ComputerName: " << eInfo->szComputerName << endl;
                cout << "SourceName: " << eInfo->szSourceName << endl;
                cout << "Strings: " << eInfo->szStrings << endl;

                if (eId >= iMaxOutPut) break;
            }
            else if (iRet == RET_ERROR_FILEID) {
                cout << "fileId Error" << endl;
            }
            else if (iRet == RET_ERROR_EID) {
                cout << "eId Error" << endl;
            }
        }
        cout << endl;

        delete eInfo;
    }
}

void DealFile(const char* filePath)
{
    //加载指定文件夹的所有日志
    LoadLogFile(filePath);
    int fileCount = GetLogFileCount();
    cout << "file count: " << fileCount << endl;

    int fileId = 0;
    //设置每个文件最大输出条数
    int         iMaxOutPut = 3;
    const char* fileName = GetLogFileName(fileId);
    if (fileName == NULL) {
        cout << "fileId Error" << endl;
        return;
    }

    const int   fileEventCount = GetLogFileEventCount(fileId);
    if (fileEventCount == RET_ERROR_FILEID) {
        cout << "fileId Error" << endl;
        return;
    }

    cout << "fileName: " << fileName << "\tEventCount: " << fileEventCount << endl;

    const auto eInfo = new EventInfo();
    for (auto eId = 0; eId < fileEventCount; ++eId) {
        int iRet = GetLogFileEvent(fileId, 0, eInfo);
        if (iRet == RET_SUCCESS) {
            cout << "Time: " << eInfo->szTime << endl;
            cout << "EventID: " << eInfo->szEventID << endl;
            cout << "EventLevel: " << eInfo->szEventLevel << endl;
            cout << "ComputerName: " << eInfo->szComputerName << endl;
            cout << "SourceName: " << eInfo->szSourceName << endl;
            cout << "Strings: " << eInfo->szStrings << endl;

            if (eId >= iMaxOutPut) break;
        }
        else if (iRet == RET_ERROR_FILEID) {
            cout << "fileId Error" << endl;
        }
        else if (iRet == RET_ERROR_EID) {
            cout << "eId Error" << endl;
        }
    }
    cout << endl;

    delete eInfo;
}

int _tmain(int argc, _TCHAR* argv[])
{
    USES_CONVERSION;

     //初始化
    if (Init()) {
        cout << "Init Success" << endl;
    }
    else {
        cout << "Init Failed" << endl;
        return -1;
    }

    string inPath;
    BOOL   bMach = FALSE;
    for (int i = 0; i < argc; ++i) {
        if (wcscmp(argv[i], L"-h") == 0 || wcscmp(argv[i], L"--help") == 0) {
            // ReSharper disable once StringLiteralTypo
            bMach = TRUE;
            cout << "LogDemo.exe -i inFolderPath(evt  evtx)" << endl;    // NOLINT(clang-diagnostic-invalid-source-encoding)
            cout << "LogDemo.exe -f inFilePath(evt  evtx)" << endl;      // NOLINT(clang-diagnostic-invalid-source-encoding)
            return 0;
        }
        else if (wcscmp(argv[i], L"-i") == 0) {
            bMach = TRUE;
            inPath = W2A(argv[++i]);
            DealFolder(inPath.c_str());
        }
        else if (wcscmp(argv[i], L"-f") == 0) {
            bMach = TRUE;
            inPath = W2A(argv[++i]);
            DealFile(inPath.c_str());
        }
    }
    if (bMach == FALSE) {
        cout << "LogDemo.exe -h" << endl;
        return 0;
    }


    Release();

    return 0;
}
