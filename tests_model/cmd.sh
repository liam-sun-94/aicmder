

curl -s 'https://member.bilibili.com/x/web/data/fan?tmid=205406148' \
  -H 'authority: member.bilibili.com' \
  -H 'pragma: no-cache' \
  -H 'cache-control: no-cache' \
  -H 'upgrade-insecure-requests: 1' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36' \
  -H 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' \
  -H 'sec-fetch-site: none' \
  -H 'sec-fetch-mode: navigate' \
  -H 'sec-fetch-user: ?1' \
  -H 'sec-fetch-dest: document' \
  -H 'accept-language: zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-TW;q=0.6' \
  -H "cookie: _uuid=7CBA7911-6CB3-3568-84CE-0D7C2616641045449infoc; buvid3=218DEC0B-BE72-47A0-B48C-195E66FC3BAA143079infoc; UM_distinctid=176462d5d0d1b3-098b52e614b34f-16386153-fa000-176462d5d0e4b5; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(k|k)RluRk)0J\'uY|~Rmlkkk; fingerprint=9aa72b916be0842bccb8f3100fa4a30f; buvid_fp=218DEC0B-BE72-47A0-B48C-195E66FC3BAA143079infoc; buvid_fp_plain=218DEC0B-BE72-47A0-B48C-195E66FC3BAA143079infoc; DedeUserID=205406148; DedeUserID__ckMd5=c5232a8ba2ec4d06; SESSDATA=1a49813b%2C1624947567%2C24f58*c1; bili_jct=1ff3bfe12d749447fa59b3564b715f8b; fingerprint3=232cb4702e9e80652ec80ed61e41de5c; fingerprint_s=3f329dea71c2a280d50a9a8a2ea1970c; PVID=1; CURRENT_QUALITY=0; bp_t_offset_205406148=487907580457283326; bp_video_offset_205406148=495574930298326570; CNZZDATA1272960325=1199544024-1610333978-https%253A%252F%252Fwww.bilibili.com%252F%7C1614560657" | python bilibili_fans.py 

# cat -n aa.txt | python bilibili_fans.py