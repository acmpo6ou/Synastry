/* gcal-debug.h.in
 *
 * Copyright (C) 2017 Georges Basile Stavracas Neto <georges.stavracas@gmail.com>
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 */

#ifndef GCAL_DEBUG_H
#define GCAL_DEBUG_H

#include <glib.h>

/**
 * SECTION:gcal-debug
 * @short_description: Debugging macros
 * @title:Debugging
 * @stability:stable
 *
 * Macros used for tracing and debugging code. These
 * are only valid when Calendar is compiled with tracing
 * suppoer (pass `--enable-tracing` to the configure
 * script to do that).
 */

G_BEGIN_DECLS

#ifndef GCAL_ENABLE_TRACE
# define GCAL_ENABLE_TRACE 0
#endif
#if GCAL_ENABLE_TRACE != 1
# undef GCAL_ENABLE_TRACE
#endif

/**
 * GCAL_LOG_LEVEL_TRACE: (skip)
 */
#ifndef GCAL_LOG_LEVEL_TRACE
# define GCAL_LOG_LEVEL_TRACE ((GLogLevelFlags)(1 << G_LOG_LEVEL_USER_SHIFT))
#endif

#ifdef GCAL_ENABLE_TRACE

/**
 * GCAL_TRACE_MSG:
 * @fmt: printf-like format of the message
 * @...: arguments for @fmt
 *
 * Prints a trace message.
 */
# define GCAL_TRACE_MSG(fmt, ...)                                        \
   g_log(G_LOG_DOMAIN, GCAL_LOG_LEVEL_TRACE, "  MSG: %s():%d: " fmt,     \
         G_STRFUNC, __LINE__, ##__VA_ARGS__)

/**
 * GCAL_PROBE:
 *
 * Prints a probing message. Put this macro in the code when
 * you want to check the program reaches a certain section
 * of code.
 */
# define GCAL_PROBE                                                      \
   g_log(G_LOG_DOMAIN, GCAL_LOG_LEVEL_TRACE, "PROBE: %s():%d",           \
         G_STRFUNC, __LINE__)

/**
 * GCAL_TODO:
 * @_msg: the message to print
 *
 * Prints a TODO message.
 */
# define GCAL_TODO(_msg)                                                 \
   g_log(G_LOG_DOMAIN, GCAL_LOG_LEVEL_TRACE, " TODO: %s():%d: %s",       \
         G_STRFUNC, __LINE__, _msg)

/**
 * GCAL_ENTRY:
 *
 * Prints an entry message. This shouldn't be used in
 * critical functions. Place this at the beggining of
 * the function, before any assertion.
 */
# define GCAL_ENTRY                                                      \
   g_log(G_LOG_DOMAIN, GCAL_LOG_LEVEL_TRACE, "ENTRY: %s():%d",           \
         G_STRFUNC, __LINE__)

/**
 * GCAL_EXIT:
 *
 * Prints an exit message. This shouldn't be used in
 * critical functions. Place this at the end of
 * the function, after any relevant code. If the
 * function returns something, use GCAL_RETURN()
 * instead.
 */
# define GCAL_EXIT                                                       \
   G_STMT_START {                                                        \
      g_log(G_LOG_DOMAIN, GCAL_LOG_LEVEL_TRACE, " EXIT: %s():%d",        \
            G_STRFUNC, __LINE__);                                        \
      return;                                                            \
   } G_STMT_END

/**
 * GCAL_GOTO:
 * @_l: goto tag
 *
 * Logs a goto jump.
 */
# define GCAL_GOTO(_l)                                                   \
   G_STMT_START {                                                        \
      g_log(G_LOG_DOMAIN, GCAL_LOG_LEVEL_TRACE, " GOTO: %s():%d ("#_l")",\
            G_STRFUNC, __LINE__);                                        \
      goto _l;                                                           \
   } G_STMT_END

/**
 * GCAL_RETURN:
 * @_r: the return value.
 *
 * Prints an exit message, and returns @_r. See #GCAL_EXIT.
 */
# define GCAL_RETURN(_r)                                                 \
   G_STMT_START {                                                        \
      g_log(G_LOG_DOMAIN, GCAL_LOG_LEVEL_TRACE, " EXIT: %s():%d ",       \
            G_STRFUNC, __LINE__);                                        \
      return _r;                                                         \
   } G_STMT_END

#else

/**
 * GCAL_TODO:
 * @_msg: the message to print
 *
 * Prints a TODO message.
 */
# define GCAL_TODO(_msg)

/**
 * GCAL_PROBE:
 *
 * Prints a probing message.
 */
# define GCAL_PROBE

/**
 * GCAL_TRACE_MSG:
 * @fmt: printf-like format of the message
 * @...: arguments for @fmt
 *
 * Prints a trace message.
 */
# define GCAL_TRACE_MSG(fmt, ...)

/**
 * GCAL_ENTRY:
 *
 * Prints a probing message. This shouldn't be used in
 * critical functions. Place this at the beggining of
 * the function, before any assertion.
 */
# define GCAL_ENTRY

/**
 * GCAL_GOTO:
 * @_l: goto tag
 *
 * Logs a goto jump.
 */
# define GCAL_GOTO(_l)   goto _l

/**
 * GCAL_EXIT:
 *
 * Prints an exit message. This shouldn't be used in
 * critical functions. Place this at the end of
 * the function, after any relevant code. If the
 * function returns somethin, use GCAL_RETURN()
 * instead.
 */
# define GCAL_EXIT       return

/**
 * GCAL_RETURN:
 * @_r: the return value.
 *
 * Prints an exit message, and returns @_r. See #GCAL_EXIT.
 */
# define GCAL_RETURN(_r) return _r
#endif

/**
 * _GCAL_BUG: (skip)
 */
#define _GCAL_BUG(Component, Description, File, Line, Func, ...)                        \
  G_STMT_START {                                                                        \
    g_printerr ("-----------------------------------------------------------------\n"); \
    g_printerr ("You've found a bug in Calendar or one of its dependent libraries.\n"); \
    g_printerr ("Please help us help you by filing a bug report at:\n");                \
    g_printerr ("\n");                                                                  \
    g_printerr ("http://bugzilla.gnome.org/enter_bug.cgi?product=gnome-calendar&component=%s\n", Component);                           \
    g_printerr ("\n");                                                                  \
    g_printerr ("%s:%d in function %s()\n", File, Line, Func);                          \
    g_printerr ("\n");                                                                  \
    g_printerr (Description"\n", ##__VA_ARGS__);                                        \
    g_printerr ("-----------------------------------------------------------------\n"); \
  } G_STMT_END

/**
 * GCAL_BUG:
 * @Component: the component
 * @Description: the description
 * @...: extra arguments
 *
 * Logs a bug-friendly message.
 */
#define GCAL_BUG(Component, Description, ...) \
  _GCAL_BUG(Component, Description, __FILE__, __LINE__, G_STRFUNC, ##__VA_ARGS__)

G_END_DECLS

#endif /* GCAL_DEBUG_H */
