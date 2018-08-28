from flask import jsonify

class APIResponse(object):
    """Base json Response with Flask jsonify and wraps as classmethod basic REST
    responses.
    """


    def _api_response(self, status_code=200, message=None, errors=[], data=[],
                      page=None):
        """Basic jsonify internal generator

        :param status_code: Response status code (200, 404, .. etc)

        :param message: Short description of response status

        :param errors: List of errors if errors

        :param data: List of returned data

        Returns a jsonify(dict), status_code Flask response.
        """
        rv_data = {
            key:value
            for (key,value) in locals().items()
            if (value or key in ['data']) and not key in ['self']
        }
        rv_data.update({"len": len(data)})
        return jsonify(rv_data), status_code

    @classmethod
    def status_400(cls, message=None, errors=[]):
        """Return status 400

        :param message: Short description of response status

        :param errors: List of errors if errors
        """
        if not message:
            message = """ The request could not be understood
                          by the server due to malformed syntax.
                      """
        return cls._api_response(cls,400, message=message, errors=errors)

    @classmethod
    def status_404(cls, message=None, errors=[]):
        """Return status 400

        :param message: Short description of response status

        :param errors: List of errors if not  errors "Not Found"
        """
        if not message:
            message = """ The requested resource was not found.
                          This can be caused by an ACL constraint
                          or if the resource does not exist. """
        if not errors:
            errors.append("Not Found")
        return cls._api_response(cls, 404, message=message, errors=errors)

    @classmethod
    def status_406(cls, message=None, errors=[]):
        """Return status 406

        :param message: Short description of response status

        :param errors: List of errors if not  errors "Not acceptable"
        """
        if not message:
            message = """The endpoint does not support the response
                         format specified in the request Accept header."""
        if not errors:
            errors = [
                "Not acceptable"
            ]
        return cls._api_response(cls, 406, message=message, errors=errors)

    @classmethod
    def status_200(cls,message=None, data=[], page=None):
        """Return status 200

        :param message: Short description of response status

        :param data: List of returned data
        """
        if not message:
            message = """Success"""

        return cls._api_response(cls, 200, message=message, data=data, page=page)

    @classmethod
    def status_201(cls, message=None, data=[]):
        """Return status 201

        :param message: Short description of response status

        :param data: List of returned data
        """
        if not message:
            message = """Created"""
        return cls._api_response(cls, 201, message=message, data=data)

    @classmethod
    def status_204(cls, message=None, data=[]):
        """Return status 200

        :param message: Short description of response status

        :param data: List of returned data
        """
        if not message:
            message = """No Content"""
        return cls._api_response(cls, 204, message=message, data=data)

    def status_418(cls):
        """Return status 418
        """
        return cls._api_response(cls, 418, message="I'm a teapot")
