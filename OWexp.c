#include <stdio.h>
#include <windows.h>
#include <stdlib.h>
#include <wchar.h>
#pragma comment(lib, "user32.lib")

#ifdef _WIN32
    #include <Windows.h>
#endif

int main(){


#ifdef _WIN32
	system("chcp 65001"); //设置字符集 （使用SetConsoleCP(65001)设置无效，原因未知）

#endif
	int k=0;
	INPUT mouseInput;
    ZeroMemory(&mouseInput, sizeof mouseInput);
	
	printf("\nOverWatch!!! Mouse Auto~~  \n## 守望先锋鼠标自动点击，刷经验专用:-)\n\n");
	printf("想关掉就直接X掉窗口~~\n\n");

    	
	float duration = 2, interval = 1;
	printf("按下鼠标的时间(秒)(Mouse Pressed Times(seconds)): ");
	scanf("%f",&duration);
	printf("松开鼠标的时间(秒)(Mouse Released Times(seconds)): ");
	scanf("%f",&interval);
	while(1){
    	mouseInput.mi.dwFlags = MOUSEEVENTF_MOVE;
    	SendInput(1, &mouseInput, sizeof(mouseInput));
    
	    mouseInput.mi.dwFlags = MOUSEEVENTF_LEFTDOWN;
    	SendInput(1, &mouseInput, sizeof(mouseInput));
    	Sleep(duration * 1000);
	    mouseInput.mi.dwFlags = MOUSEEVENTF_LEFTUP;
	    SendInput(1, &mouseInput, sizeof(mouseInput));
	    Sleep(interval * 1000);
	}
	scanf("%d", &k);
	return 0;
}