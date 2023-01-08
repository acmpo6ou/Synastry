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
libecal_dep = dependency('libecal-2.0', version: '>= 3.33.2')
gtk_dep = dependency('gtk+-3.0', version: '>= 3.22.20')
gio_dep = dependency('gio-2.0', version: '>= 2.58.0')
goa_dep = dependency('goa-1.0', version: '>= 3.2.0')
libdazzle_dep = dependency('libdazzle-1.0', version: '>= 3.33.1')

library(
  'gcal',
  sources: sources,
  dependencies: [glib_dep, libecal_dep, gtk_dep, gio_dep, goa_dep, libdazzle_dep]
)
