project('gcal', 'c')

calendar_incs =  include_directories('.')
gnome = import('gnome')

built_sources = gnome.compile_resources(
  'views-resources',
  'views.gresource.xml',
  c_name: 'views',
)

sources = files(
  'gcal-month-cell.c',
  'gcal-month-popover.c',
  'gcal-month-view.c',
  'gcal-view.c',
)

glib_dep = dependency('glib-2.0', version: '>= 2.67.5')
library('gcal', sources: sources, dependencies: [glib_dep])
