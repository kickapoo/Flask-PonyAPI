import re
from flask import request, url_for
from flask_ponyapi.responses import APIResponse
from pony.orm import db_session, commit, ObjectNotFound


class Meta:
    pass

class RestEntity(object):
    """Main REST constructorself.
    
    :param app: Flask application object

    :param entity: Pony Entity object.

    """

    def __init__(self, app, entity):
        self.app = app
        self.entity = entity

        self._setup_meta(entity)
        self._make_rest(entity)

    def _setup_meta(self, entity):
        """Create a _meta object with entity meta information.
        """
        self._meta = Meta() # Make an empty Class in order to use dot notation
        if hasattr(self.entity, 'Meta'):
            self._meta = entity.Meta
        self._meta.attrs = self._entity_attrs(entity)
        self._meta.attrs_names = [e['attr'] for e in self._meta.attrs]
        self._meta.rqd_attrs = [
            e['attr'] for e in self._meta.attrs
            if e['rqd'] and not e['pk']
        ]
        self._meta._pk = self.entity._pk_.name
        self._meta.base_rule = self._build_rule()
        return

    def _entity_attrs(self, entity):
        """Return entity fields details: name, is_required, is_pk, is_unique,
           type.
        """
        return [
            {
                'attr': e.name,
                'rqd': e.is_required,
                'pk': e.is_pk,
                'unique': e.is_unique,
                'type': e.py_type.__name__
            }
            for e in entity._attrs_
        ]

    def _validate_request_querystrings(self):
        """Validate incoming request querystrings. If not ?fields defined add
        all Entity fields.
        """
        fields = request.args.get('fields', None)
        if not fields:
            fields = self._meta.attrs_names
        page = request.args.get('page', None)
        if not page:
            page = 1
        # if not self._meta._pk in fields:
        #     fields += ',' + self.entity_pk
        return fields, page

    def _validate_request_args(self, data):
        """Validate incoming request args. Check if incoming post/put data have
        unrelated fields or all required fields are set and return errors if any.
        """
        # Are incoming request args in entity fields list?
        if set(data.keys()).difference(set(self._meta.attrs_names)):
            unrelated_fields = list(
                set(data.keys()).difference(set(self._meta.attrs_names))
            )
            return ["Un-Related Field: {}".format(f) for f in unrelated_fields]
        # Are all rqd fields in incoming args ?
        if not set(self._meta.rqd_attrs).issubset(set(data.keys())):
            missing_fields = list(
                set(self._meta.rqd_attrs).difference(set(data.keys()))
            )
            return ["Field Required: {}".format(f) for f in missing_fields]
        return

    def _route_rule(self, endpoint):
        """Flask endpoints are unique like table names and follow Entity:method.
        For example,  Person:get . This way endpoint can be references like
        nornal flask endpoint for example in redirect, redirect('Person:get')
        """
        return "{}:{}".format(self.entity.__name__, endpoint)

    def _build_rule(self):
        """Build the url rule based on Entity._meta (Class Meta) attributes
        - route_prefix
        - route_base

        ... example:
        class Meta:
            route_prefix="persons"
            route_base='/api'

        will create: /api/persons (list, get) /api/persons (put, delete)

        """
        rule_parts = []
        if hasattr(self._meta, 'route_prefix'):
            rule_parts.append(self._meta.route_prefix)
        if hasattr(self._meta, 'route_base'):
            rule_parts.append(self._meta.route_base)
        else:
            rule_parts.append(self.entity.__name__.lower())
        result = "/{}".format("/".join(rule_parts))
        return re.sub(r'(/)\1+', r'\1', result)

    def _make_rest(self, entity):
        """Register Entity model to app.rules map.
        :param entity: The db.Entity (what else ?)
        """
        endpoints = ['list', 'get', 'post', 'put', 'delete']
        for endpoint in endpoints:
            view_func = getattr(self, endpoint)
            methods = [endpoint.upper()]
            route_rule = self._route_rule(endpoint)
            if endpoint in ['list', 'post']:
                self.app.add_url_rule(self._meta.base_rule, route_rule, view_func)
                if endpoint == 'post':
                    self.app.add_url_rule(self._meta.base_rule,
                        route_rule, view_func, methods=methods)
            else:
                self.app.add_url_rule(self._meta.base_rule+"/<pk>",
                    route_rule, view_func, methods=methods)
        return

    def _get_endpoint(self, entity_record):
        """Wrapper for flask url_for function for a single Entity"""
        return url_for(self._route_rule('get'), pk=entity_record.get_pk(),
                      _external=True)

    @db_session
    def _get_entity_or_None(self, pk):
        """Helper for get or Not Found Response"""
        try:
            entity = self.entity[pk]
        except ObjectNotFound:
            return None
        return entity

    @db_session
    def list(self):
        """List / Index endpoint"""
        fields, page = self._validate_request_querystrings()
        data = []
        for e in self.entity.select().page(int(page), 20):
            res = e.to_dict(fields)
            res.update({"url": self._get_endpoint(e)})
            data.append(res)
        return APIResponse.status_200(data=data, page=page)

    @db_session
    def get(self, pk):
        """Get Endpoint"""
        fields, page = self._validate_request_querystrings()
        entity = self._get_entity_or_None(pk)
        if not entity:
            return APIResponse.status_404()
        return APIResponse.status_200(
            data=self.entity.get(**{self._meta._pk: pk}).to_dict(fields)
        )

    @db_session
    def post(self):
        """Post Endpoint"""
        args = request.get_json(force=True, silent=True)
        if not args:
            return APIResponse.status_400(errors=["Empty post args fields"])
        errors = self._validate_request_args(args)
        if errors:
            return APIResponse.status_400(errors=errors)
        try:
            newentity = self.entity(**args)
            # commit and clear db transaction session
            # basically , get pk
            commit()
            data = newentity.to_dict()
            data.update({"url": self._get_endpoint(newentity)})
        except Exception as e:
            return APIResponse.status_400(errors=[str(e)])
        return APIResponse.status_201(data=data)

    @db_session
    def put(self, pk):
        """Put endpoint"""
        args = request.get_json(force=True, silent=True)
        entity = self._get_entity_or_None(pk)
        if not entity:
            return APIResponse.status_404()
        entity.set(**args)
        return APIResponse.status_204(data=entity.to_dict())

    @db_session
    def delete(self, pk):
        """Delete endpoint"""
        entity = self._get_entity_or_None(pk)
        if not entity:
            return APIResponse.status_404()
        entity.delete()
        return APIResponse.status_204()
