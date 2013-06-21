CC = /home/jwn02/project/openwrt/sdk/staging_dir/toolchain-mips_r2_gcc-4.6-linaro_uClibc-0.9.33.2/bin/mips-openwrt-linux-uclibc-gcc
INCLUDE =/home/jwn02/project/openwrt/sdk/staging_dir/toolchain-mips_r2_gcc-4.6-linaro_uClibc-0.9.33.2/include
LIBRARY = /home/jwn02/project/openwrt/sdk/staging_dir/toolchain-mips_r2_gcc-4.6-linaro_uClibc-0.9.33.2/lib

ALL : 
	$(CC) -o server epoll_server.c  -I $(INCLUDE) -L $(LIBRARY) -lpthread

