// +build openbsd
// +build 386 amd64 arm arm64

package pty

type ptmget struct {
	Cfd	int32
	Sfd	int32
	Cn	[16]int8
	Sn	[16]int8
}

var ioctl_PTMGET = 0x40287401
