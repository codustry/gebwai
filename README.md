# Gebwai


## Features

- เก็บข้อมูล เท่าที่จำเป็น ไม่มีแอบ
    - ตรวจสอบ source code ได้เต็มที่ ถาม AI ให้ช่วยท่านอ่านให้ก็ได้ 
    - TODO: #2 ใช้ [Sigstore](https://www.sigstore.dev/) เพื่อยืนยันว่า source code กับที่ deploy เป็นอันเดียวกัน

## Development

To get started, you need to have the following tools installed:

- install mise as version manager and task runner
- install [cloudflared](https://github.com/cloudflare/cloudflared) as reverse proxy

- `.tpl` is meant to use with 

### Expose Localhost
There are many ways to expose localhost to the internet. We prefer `cloudflared tunnel`. Please follow [https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/get-started/create-local-tunnel/] for more detail.

*Install*

```sh {"id":"01HZXBKK8AYBF7P6440EVFJMN7"}
mise use -g ubi:cloudflare/cloudflared@2024.6.0
```

*login*

```sh {"id":"01HZXBN8RDFK0T4TFJ3SZFEBJW"}
cloudflared tunnel login
```

*create tunnel*

```sh {"id":"01HZXBRRHN8XQ7YXW943W96A45"}
cloudflared tunnel create gebwai-development-tunnel
```

```sh {"id":"01HZY3T3ZJF2CR71WX5ASQB760"}
cloudflared tunnel route dns gebwai-development-tunnel dcd64c02.gebwai.com
```

```sh {"id":"01HZY3Z39PPTM3N0Q3NE49JXMV"}
cloudflared tunnel --config Deployment/cloudflare_tunnel_config.yml run gebwai-development-tunnel
```

## Gebwai Co-Creation
>  🐿 ช่วยกันเลี้ยง "เก็บไว้" ให้โตเป็นผู้ใหญ่ที่ดีกันน 🤗

สถานที่ที่ให้ user ทุกคนได้แลกเปลี่ยนพูดคุย🗣 แลกเปลี่ยน เทคนิคการใช้งานต่างๆ ปัญหา ข้อกังวล และโหวดฟีเจอร์ใหม่ๆ❎ สามารถพบเจอกับนักพัฒนาตรงๆได้ที่นี้อีกด้วย เข้า Discussion เพื่อเริ่มคุยได้เลย

### ทุนนิยกตัญญูตา - [Compassionate Capitalism](https://www.perplexity.ai/search/could-you-advice-tjFxIvpvS8GAJSPaiihBvg)
> a Codustry Pilot Project by Nutchanon Ninyawee(Ben)

ขอบคุณด้วยเงิน มีน้อยแบ่งน้อยมีมากแบ่งมาก แบ่งเงินกำไรส่วนหนึ่งให้กับ Contributors, Security Auditors🛡🔐 และ Upstream Dependency Orgs ในระยะแรก Author จะตัดสินใจชั่งน้ำหนักส่วนแบ่งให้



## License

This project is on Functional Source License, Version 1.1, ISC Future License.


