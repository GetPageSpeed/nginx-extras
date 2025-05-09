# nginx-extras

![CircleCI](https://circleci.com/gh/GetPageSpeed/repotest.svg?style=shield&circle-token=db54937e3be24afebb2520f2c59ecb65a848900d)

The [nginx-extras](https://www.getpagespeed.com/nginx-extras) project, as part of [GetPageSpeed repositories](https://www.getpagespeed.com/redhat) 
is your source of secure, well-maintained packages of NGINX and its 50+ modules.

Production-ready, quality binary RPM packages for NGINX Brotli, PageSpeed, dynamic ETags, ModSecurity modules (and many more),
all available for installation via `yum/dnf`, giving you ability to configure your ultimate performant and secure NGINX setup.

Available by [subscription](https://www.getpagespeed.com/repo-subscribe), 
it is a budget NGINX Plus alternative, for any RPM-based distro!

For sysadmins this allows to:

* install prebuilt CentOS/RHEL packages for virtually any NGINX module, without compilation
* save time, any module can be installed in seconds
* save production systems from pollution by compilation software

For module authors, this allows to:

* deliver your module as an installable package *in ten minutes*
* automatic rebuilds when you tag a new release of your module (within 24 hrs)
* automatic rebuilds against newly released NGINX versions

## Supported architectures

* x86_64
* aarch64 (ARM64)

## Install any NGINX module whatsoever in any RPM-based distro

We provide NGINX module RPM packages for:

* CentOS/RHEL
* Fedora Linux (**and this one is free**)
* Amazon Linux
* Suse Linux

To verify the integrity of packages before installing, [import our GPG key first](https://nginx-extras.getpagespeed.com/integrity/).

### Step 1. Install repository configuration for your OS

    yum -y install https://extras.getpagespeed.com/release-latest.rpm

### Step 2. Enable installing modules for mainline NGINX (if you must)

    yum -y install yum-utils
    yum-config-manager --enable getpagespeed-extras-mainline

### Step 3. Install the module, e.g. cache-purge     

    yum -y install nginx-module-cache-purge

## Request a module

The list of modules we discovered on GitHub but haven't yet tested or packaged is [here](docs/nonpackaged-modules.md). 
You can open a ticket/issue to request packaging of any of those.

## Module Requirements (for authors)

The module requirements are pretty straightforward, and most of the module repositories already follow it:

* Hosted on GitHub
* Tag releases with sensible version numbers. Repositories without any version tag can't build. Pre-releases / beta versions are detected and *not* built
* `config` file in the root of repository *must* support compiling as dynamic module

### Submit your module for build

* Fork the repository
* Create `modules/<handle>.yml` file and specify parameters like the example below. The handle should be unique. The resulting package will have name `nginx-module-<handle>`, e.g. `nginx-module-foo`
* Submit a pull request. That's it! Your module will be automatically built against both stable and mainline NGINX. Check it within 10 mins [here](https://extras.getpagespeed.com/redhat/7/mainline/x86_64/repoview/letter_n.group.html) (for mainline NGINX) and [here](https://extras.getpagespeed.com/redhat/7/x86_64/repoview/letter_n.group.html) (for stable NGINX). If it doesn't appear, [raise an issue](https://github.com/GetPageSpeed/nginx-extras/issues/new).

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

* `repo` (required): GitHub repository in format `<owner>/<name>`
* `summary`: short (up to 70 characters) summary of the module
* `description`: longer description of the module
* `soname` (required): basename of dynamic module filename
* `release_ticket`: a URL to the original GitHub project, requesting to tag a release. 
  This is the way to link back to the original project when we have to fork it for the sake of packaging or
  including important fixes 
* `build_requires` allows you to specify external devel library dependencies, e.g.:

```yml 
build_requires:
  - hiredis-devel
```

Version is automatically detected from your latest release, using [`lastversion`](https://github.com/dvershinin/lastversion).
Make sure that your latest release has a `LICENSE` if you want it to be included in resulting RPM!

## Caveats (for module authors)

Some modules have a pretty sophisticated RPM logic. 
One is example is `nginx-module-pagespeed`: it needs custom SELinux policy, among other things.
Don't worry, we still build those modules elsewhere, and 
they are available through our repository same as any module that is built through this system.

If your module is one of those, raise an issue here.

99% of modules can be still built through this system.

## Caveats (for sysadmins)

Using our repository implies you take all the risks associated with using an unofficial repository.
Purchase Nginx Plus subscription if not sure :)
