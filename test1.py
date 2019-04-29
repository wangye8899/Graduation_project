import requests
import json

data = {'code':'#include <stdio.h>int main(){ /* 我的第一个 C 程序 */printf("Hello, World! ");return 0;}','language':'7','fileext':'c'}

res = requests.post("https://www.runoob.com/api/compile.php",data=data)

print(res.json())

"""
code: #include <stdio.h>

int main()
{
   /* 我的第一个 C 程序 */
   printf("Hello, World! \n");
   
   return 0;
}
language: 7
fileext: c
"""