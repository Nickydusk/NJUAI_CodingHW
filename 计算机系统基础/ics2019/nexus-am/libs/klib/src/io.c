#include <klib.h>
#include <amdev.h>

uint32_t uptime() {
  _DEV_TIMER_UPTIME_t uptime;
  _io_read(_DEV_TIMER, _DEVREG_TIMER_UPTIME, &uptime, sizeof(uptime));
  return uptime.lo;
} // 返回系统启动后经过的毫秒数  

void get_timeofday(void *rtc) {
  _io_read(_DEV_TIMER, _DEVREG_TIMER_DATE, rtc, sizeof(_DEV_TIMER_DATE_t));
} // 在`rtc`结构中返回当前时间, PA中不会用到

int read_key() {
  _DEV_INPUT_KBD_t key;
  _io_read(_DEV_INPUT, _DEVREG_INPUT_KBD, &key, sizeof(_DEV_INPUT_KBD_t));
  int ret = key.keycode;
  if (key.keydown) ret |= 0x8000;
  return ret;
} // 返回按键的键盘码, 若无按键, 则返回`_KEY_NONE`

void draw_rect(uint32_t *pixels, int x, int y, int w, int h) {
  _DEV_VIDEO_FBCTL_t ctl = (_DEV_VIDEO_FBCTL_t) {
    .pixels = pixels,
    .x = x, .y = y, .w = w, .h = h,
    .sync = 0,
  };
  _io_write(_DEV_VIDEO, _DEVREG_VIDEO_FBCTL, &ctl, sizeof(ctl));
} // 将`pixels`指定的矩形像素绘制到屏幕中以`(x, y)`和`(x+w, y+h)`两点连线为对角线的矩形区域

void draw_sync() {
  _DEV_VIDEO_FBCTL_t ctl;
  ctl.pixels = NULL;
  ctl.x = ctl.y = ctl.w = ctl.h = 0;
  ctl.sync = 1;
  _io_write(_DEV_VIDEO, _DEVREG_VIDEO_FBCTL, &ctl, sizeof(ctl));
} // 将之前的绘制内容同步到屏幕上

int screen_width() {
  _DEV_VIDEO_INFO_t info;
  _io_read(_DEV_VIDEO, _DEVREG_VIDEO_INFO, &info, sizeof(info));
  return info.width;
} // 宽

int screen_height() {
  _DEV_VIDEO_INFO_t info;
  _io_read(_DEV_VIDEO, _DEVREG_VIDEO_INFO, &info, sizeof(info));
  return info.height;
} // 高