---
title: Hosting a static website on IPFS
date: 2025-02-15 08:50:12 +0100
draft: false
tags: [Work, ipfs, tutorial, hugo, website]
---
In the [previous blog post]({{< relref "/blog/2025/ipfs" >}}), I covered the basic principles of IPFS and its features. In this article, I'm going to explore a more advanced use case—hosting a static website on IPFS.

Before diving in, I'd like to briefly explain the difference between dynamic and static websites.

For dynamic websites, content is generated on the fly by a program. These programs are typically written in languages like PHP, JavaScript, Python, or Go. When a browser makes a request, a web server processes it and forwards it to the program, which then dynamically generates an HTML page and returns it to the user. This means that requests from _different users_ to the _same URL_ can result in _different responses_. This approach makes sense when the same URL needs to serve personalized content. For example, in social networks, the same news feed page shows different updates to different users.

For static websites, all HTML files are pre-generated and stored in the server’s file system. All requests are handled by the web server, just like with a dynamic site, but instead of running additional programs, the web server simply reads and returns HTML files directly from disk. As a result, _different users_ requesting the _same URL_ receive exactly the _same response_. This is the simplest, fastest, and most reliable way to serve data, making it an excellent choice for blogs like this one (though there are far more complex examples of static websites out there).
![Dynamic site vs static](dynamic-vs-static-2.png)

IPFS is a distributed file storage system; it can't serve dynamic websites, but it works fine for static ones. Essentially, a static website is just a directory with HTML, CSS, JS files, and images. To host such a site on IPFS, all you need to do is add the files to the system using a command like `ipfs add ...`. However, there are a few nuances I'd like to cover.

To make a static website accessible via IPFS, follow these four steps:
1. Run an _ipfs daemon_.
2. Use relative links to local resources in HTML files.
3. Add _dnsLink_.
4. Use _IPNS_ and enable auto-refresh.

Actually, only the first two steps are required, but the remaining two make accessing the site more convenient. Further on, I'll go into more detail about each step.
{{< more >}}
<!--more-->

### ipfs daemon
Before setting up access to the IPFS version of the website, it's important to note that the _ipfs daemon_ must be running on the server handling IPFS requests for the site. The _ipfs daemon_ is a program that implements the IPFS protocol. It listens on several network ports, the most important being:
- `4001` — handles IPFS requests,
- `8080` — local web gateway,
- `5001` — web UI.

The `4001` port must be accessible from the internet; otherwise, other IPFS nodes won't be able to find your node. The `8080` port should also be open, but it's best to place a reverse proxy in front of it. I'll cover this in more detail later. Access to port `5001` **MUST BE blocked from the internet!**

### Internal links
Imagine, we have a `public` directory with the following file hierarchy:
```bash
public
├── index.html
├── blog
│   └── 2025
│       └── ipfs
│           └── index.html
├── css
│   └── styles.css
├── js
│   └── scripts.js
└── img
    └── logo.png
```

What would a link from `blog/2025/ipfs/index.html` to `img/logo.png` look like? There are two ways to create such a link:
- Relative to the website's root: `/img/logo.png`
- Relative to the current directory: `../../../img/logo.png`

In general, if we're not talking about publishing a website to IPFS, the first approach is preferable—it's shorter and easier to read. However, in our case, only the link relative to the current directory will work. Let's break down why.

I [already mentioned]({{< relref "/blog/2025/ipfs/#using-the-official-ipfs-client" >}}) the `ipfs add <filename>` command, which adds a file to IPFS. To add the contents of a directory, use the `-r` flag: `ipfs add -r <dirname>`. With this flag, a CID is computed for each file and subdirectory, and all of them are published in IPFS.

One key property of IPFS is that when you add a directory to the system,

> each file in the directory can be accessed either by its own CID or by its path relative to the root directory's CID!

Let's say, after adding this directory to IPFS we got the following CIDs:
|path|CID|
|----|---|
| `public/img/logo.png`|`qwe456`|
| `public`|`abc123`|

Using the CLI tool, the file `logo.png` can be retrieved with two ways:
|CID|command|
|---|-------|
|by using file's CID|`ipfs get qwe456`|
|by using directory's CID|`ipfs get abc123/img/logo.png`|

If we use a web gateway like `https://ipfs.io`, the file will be accessible at:
- `https://ipfs.io/ipfs/qwe456`
- `https://ipfs.io/ipfs/abc123/img/logo.png`

Now, let's imagine that from `blog/2025/ipfs/index.html`, we add a link to the logo as `/img/logo.png`. With a web gateway, the absolute path to the logo would be `https://ipfs.io/img/logo.png`, but this file obviously doesn't exist.

However, if we use the path `../../../img/logo.png` for the logo, it will resolve to `https://ipfs.io/ipfs/abc123/blog/2025/ipfs/../../../img/logo.png`, which equals to `https://ipfs.io/ipfs/abc123/img/logo.png`, making the file accessible.

Thus, one of the key requirements for a website published on IPFS is:

> local resources must be referenced using only relative paths to the current directory.

In the context of IPFS, there's another way to link from `blog/2025/ipfs/index.html` to `img/logo.png`. We can use an IPFS path like `/ipfs/qwe456`, but the downside of this approach is that such links won't work when serving the content with a regular web server. With the configuration described above:

> the same HTML files can be used both for direct HTTP access and for serving via IPFS.

For this blog, I use the Hugo static site generator, and to enable relative links, I just need to set `relativeURLs = true` in the configuration file. I'm pretty sure other site generators have a similar option.

Technically, I could end this article here. If your static site uses relative links, you can publish it with `ipfs add -r <dirname>`, and it will be available on IPFS. However, there are a couple of key optimizations that can make the IPFS version of the site less resource-intensive and more accessible. I'll cover them in the next sections.

### --nocopy

Let's take a look at one key argument of the `ipfs add` command. In the previous blog post, I [mentioned]({{< relref "/blog/2025/ipfs/#how-ipfs-stores-data" >}}) that by default, when a new file is added to IPFS, the original file stays in place, while a copy of it, split into 256 KB blocks, is stored in the IPFS metadata directory. IPFS distributes this copy, not the original file.

Such an approach is often impractical. For example, in my case, the website's files take up around 10 GB  
(_by the way, shoutout to the Hugo developers who [don’t consider it a bug](https://discourse.gohugo.io/t/hugo-creates-a-copy-of-each-image-for-each-translated-version-of-a-page/42922)  
that identical static files are duplicated across different language versions of the site_). Duplicating this data may increase hosting costs, so it's best to avoid it.

Here, the experimental `--nocopy` flag can be useful--it allows IPFS to serve content directly from the original files. With this flag, instead of copying file chunks to the metadata directory, IPFS will store references to the original files there. These metadata entries still take up some space, but the total storage usage will be 10–100 times smaller than without this flag.

The `--nocopy` option requires the file system to support _mmap_ and stable _inodes_. Linux file systems like Ext4, XFS, and ZFS support this. To enable this option, you need to [enable filestore](https://github.com/ipfs/kubo/blob/ddfd776a99eb585538fcf5de152a9636c1ccb5bd/docs/experimental-features.md#ipfs-filestore):
```bash
romka@laptop:~$ ipfs config --json Experimental.FilestoreEnabled true
```

Now, the complete command to add files to IPFS will be:
```bash
romka@laptop:~$ ipfs add -r --nocopy <dirname>
```

In my case, the website contains about 13,000 files, and the metadata takes up around 100 MB, while the original files occupy roughly 10 GB.

It's important to note that without `--nocopy`, deleting the original file won't remove it from IPFS, whereas with `--nocopy`, it will.

### Accessing the website via a local web gateway

The `ipfs add -r --nocopy <dirname>` command prints a full list of processed files and their CIDs to stdout. In my case, processing the files takes around 5 minutes. The last line of the output contains the root directory's CID—this is the key part. Copy this CID and use it to access the site via any web gateway, for example: `https://ipfs.io/ipfs/<CID>`.

Unfortunately, with the current configuration, the website will be painfully slow, since the content is served by only a single node, and file lookup in IPFS isn't fast. There’s a good chance that, every now and then, requests to the site via public web gateways will hit a _504 Gateway Timeout_ error. To fix this, you need to set up access to the local web gateway. I don’t recommend exposing port `8080` to the open internet. Instead, it's better to set up a subdomain handled by Nginx, which will proxy all requests to the IPFS daemon.

In my case the configuration is trivial:
```
server {
    listen 80;
    server_name ipfs.romka.eu;
    
    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

With this setup, the IPFS version of the website can be accessed at `http://ipfs.romka.eu/ipfs/<CID>`. It works just like `https://ipfs.io`, but my gateway doesn't have to perform costly lookups to find my website's files since they're already on the same server.

By default, such a gateway allows access to any content in IPFS, but that's not what I want. I run my website on a cheap virtual machine, and its resources aren't enough to act as a full-fledged IPFS gateway. That's why I configured it to [serve only local data](https://github.com/ipfs/kubo/blob/ddfd776a99eb585538fcf5de152a9636c1ccb5bd/docs/config.md#gatewaynofetch).:
```bash
romka@laptop:~$ ipfs config --json Gateway.NoFetch true
```

### dnslink

With the setup from the previous section, pages from the website will be accessible via the local web gateway at URLs like `http://ipfs.romka.eu/ipfs/<CID>`. This isn’t very convenient: users not only need to know the gateway’s address, but also the CID of the front page, which changes with every content update.

To solve this issue, [dnslink](https://dnslink.dev/) can be used. Originally developed by the IPFS authors, dnslink is now adopted by other distributed systems as well.

The idea is simple: in the DNS settings, you can add a `TXT` record with a name like `_dnslink.<hostname>` and a value of `dnslink=/ipfs/<CID>` or `dnslink=/ipns/<IPNS-hash>`.

With these settings, each time the IPFS daemon receives a request for `<hostname>`, it fetches the default CID or IPNS entry linked to the requested hostname from DNS. As a result, site visitors don't need to remember the front page's CID -- it’s automatically pulled from DNS.

### IPNS
With dnslink, the responsibility of specifying the website's front page CID shifts from users to the website developer. If an IPFS link is used in dnslink, the DNS entry will have to be updated every time the site is updated. This is inconvenient, so it's better to use IPNS -- InterPlanetary Name System—here instead. I already mentioned it in the [previous blog post]({{< relref "/blog/2025/ipfs/#but-why-is-data-immutable-and-what-is-the-point-in-it" >}}). 

The idea is simple: each IPFS node has a unique cryptographic key, and a permanent IPNS alias associated with this key can be created for each node. This IPNS alias can be linked to any CID. Then, instead of a CID, an IPNS alias can be used in dnslink. If the front page's CID changes, it's enough to update the IPNS record with the command `ipfs name publish /ipfs/<NewCID>`, eliminating the need to modify the DNS settings.

In my case, DNS settings look like this:
```
ipfs            CNAME   romka.eu
_dnslink.ipfs   TXT     dnslink=/ipns/k51qzi5uqu5dizn6ymg87i7ni9oieklsqgchw1qk5lnr6ln88abocxg9ifv0cb
```
With these settings, the IPFS version of this blog is accessible at `http://ipfs.romka.eu`, or via public web gateways using a link like `https://ipfs.io/ipns/k51qzi5uqu5dizn6ymg87i7ni9oieklsqgchw1qk5lnr6ln88abocxg9ifv0cb/`.

It's important to keep in mind that IPNS records have a limited Time To Live (TTL)—by default, 24 hours—so it's necessary to set up automatic updates for them. This can be achieved with the following configuration:
```bash
romka@laptop:~$ ipfs config --json Ipns.UsePubsub true
```

### Conclusion

That's it! Once these steps are done, your website will be live on IPFS.

As I mentioned in my previous post, IPFS is still a niche solution, and hosting websites on it is more of an experiment than a practical choice. But who knows—maybe in the future, it will gain broader adoption.
