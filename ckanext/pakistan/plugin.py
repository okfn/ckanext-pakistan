import os
import logging
import ckan.plugins as p
import ckan.plugins.toolkit as toolkit
import ckanext.pakistan.icons as icons

ignore_missing = toolkit.get_validator('ignore_missing')

log = logging.getLogger(__name__)


class PakistanCustomizations(p.SingletonPlugin):
    p.implements(p.IRoutes)
    p.implements(p.IConfigurer, inherit=True)
    p.implements(p.IConfigurable, inherit=True)
    p.implements(p.IPackageController, inherit=True)
    p.implements(p.ITemplateHelpers)

    def update_config(self, config):
        here = os.path.dirname(__file__)
        rootdir = os.path.dirname(os.path.dirname(here))

        our_public_dir = os.path.join(rootdir, 'ckanext', 'pakistan', 'theme',
                'public')
        template_dir = os.path.join(rootdir, 'ckanext', 'pakistan', 'theme',
                'templates')
        config['extra_public_paths'] = ','.join([our_public_dir,
                config.get('extra_public_paths', '')])
        config['extra_template_paths'] = ','.join([template_dir,
                config.get('extra_template_paths', '')])

        toolkit.add_resource('theme/resources', 'pakistan-theme')

        from ckanext.pages.actions import schema
        extra_schema = {"icon": [ignore_missing, unicode],
                        "category": [ignore_missing, unicode],
                        "homepage_order": [ignore_missing, unicode]}
        schema.update(extra_schema)
        config['ckanext.pages.form'] = 'pages_form.html'

    def before_map(self, route_map):
        return route_map

    def after_map(self, route_map):
        return route_map

    def get_helpers(self):
        return {'icon_list': self.get_icons,
                'homepage_order': self.order_list,
                'get_homepage_icons': self.get_homepage_icons}

    def order_list(self):
        icon_list = [('', 'No Homepage Order')]
        for num in range(1, 11):
            icon_list.append((str(num), str(num)))
        return icon_list

    def get_icons(self):
        icon_list = [('', 'No Icon')]
        for icon in sorted(icons.icons):
            icon_list.append((icon, icon[5:]))
        return icon_list

    def get_homepage_icons(self):
        pages = toolkit.get_action('ckanext_pages_list')({}, {'page_type': 'page',
                                                              'private': False})
        homepage_pages = []
        for page in pages:
            if (not page.get('icon') or
                not page.get('category') or
                not page.get('homepage_order')):
                continue
            try:
                page['homepage_order'] = int(page['homepage_order'])
            except ValueError:
                continue
            homepage_pages.append(page)

        return sorted(homepage_pages, key=lambda page: page['homepage_order'])
