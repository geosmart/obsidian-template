---
draft: true
title: memos
tags: []
created: 2024-11-28T17:46:24
updated: 2025-03-19T21:05:53
---

# memos
<%*
// template desc: fetch recently fleet note from self-hosted memos rest api to obsidian note.

// load memos from memos service
const apiUrl = 'http://geosmart.duckdns.org:15230/api/memo';
// can reset by memos admin
const openId="13016c23-b912-4c8b-a330-8c41a39bc098";

// query offset
const offset=0;
const limit=20;
// only return memos in 2 days ,means
const limit_days=2;
const output = await tp.user.memos(apiUrl,openId,offset,limit,limit_days);
if(output){
 tR = output;
}
%>
