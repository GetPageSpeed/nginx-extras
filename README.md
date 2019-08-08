# nginx-extras

The nginx-extras project is your freeware Nginx Plus!

It allows you to:

* install prebuilt CentOS/RHEL packages for virtually any NGINX module, without compilation
* submit *your* NGINX module for build in GetPageSpeed extras RPM repository

## Install any module whatsoever in CentOS/RHEL 6/7

### Step 1. Install repository configuration for your OS

    yum install https://extras.getpagespeed.com/release-el$(rpm -E %{rhel})-latest.rpm

### Step 2. Enable installing modules for mainline NGINX (if you must)

    yum -y install yum-utils
    yum-config-manager --enable getpagespeed-extras-mainline

### Step 3. Install the module, e.g. cache-purge     

    yum install nginx-module-cache-purge

## Module Requirements (for authors)

The module requirements are pretty straightforward and most of module repositories already follow it:

* Hosted on GitHub
* Tag releases with sane version numbers. Repositories without any version tag can't build. Pre-releases / beta versions are detected and *not* built
* `config` file in the root of repository *must* support compiling as dynamic module

### Submit your module for build

* Fork the repository
* Create `modules/<handle>.yml` file and specify parameters like the example below. The handle should be unique. The resulting package will have name `nginx-module-<handle>`, e.g. `nginx-module-foo`
* Submit pull request. That's it! Your module will be automatically built against both stable and mainline NGINX. Check it within 30 mins [here](https://extras.getpagespeed.com/redhat/7/mainline/x86_64/repoview/letter_n.group.html) (for mainline NGINX) and [here](https://extras.getpagespeed.com/redhat/7/x86_64/repoview/letter_n.group.html) (for stable NGINX). If it doesn't appear, [raise an issue](https://github.com/GetPageSpeed/nginx-extras/issues/new).

### Sample module.yml

```yml
repo: openresty/srcache-nginx-module
summary: Transparent subrequest-based caching layout for arbitrary NGINX locations
description: |
  This module provides a transparent caching layer for arbitrary nginx
  locations (like those use an upstream or even serve static disk files).

  The caching behavior is mostly compatible with RFC 2616.
soname: ngx_http_srcache_filter_module
```

* `repo`: GitHub repository in format `<owner>/<name>`
* `summary`: short (up to 70 characters) summary of the module
* `description`: longer description of the module
* `soname`: basename of dynamic module filename

Version is automatically detected from your latest release, using [`lastversion`](https://github.com/dvershinin/lastversion).
Make sure that your latest release has a `LICENSE` if you want it to be included in resulting RPM!
