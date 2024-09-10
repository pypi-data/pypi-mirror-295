
# Django Nigerians Only

**Django Nigerians Only** is a third-party Django application that restricts access to Django applications to only Nigerian users. It can be extended to other countries with a few simple steps.

## Requirements

- Django >= 4.1
- geoip2 >= 4.8.0

## Installation

1. **Install Nigerian Only** using pip:

   ```bash
   pip install django-nigerians-only
   ```

2. **Add `'nigerian_only'` to `INSTALLED_APPS`** in your Django project's `settings.py`:

   ```python
   INSTALLED_APPS = [
       ...
       'nigerian_only',
   ]
   ```

3. **Add the middleware** to `MIDDLEWARE` in `settings.py`:

   ```python
   MIDDLEWARE = [
       ...
       'nigerian_only.middleware.NigeriansOnlyMiddleware',
   ]
   ```

4. **Whitelist allowed countries** by setting the list of allowed countries using ISO Alpha-2 country codes. [Find Country Codes Alpha-2 & Alpha-3 here](https://www.iban.com/country-codes).

   ```python
   WHITELISTED_COUNTRIES = ["NG"]  # Example: "NG" for Nigeria
   ```

5. **Download the GeoIP2 database** from [MaxMind](https://dev.maxmind.com/geoip/geoip2/geolite2/) and set the path in `settings.py`. You can read more on setting up GeoIP for Django [here](https://docs.djangoproject.com/en/5.1/ref/contrib/gis/geoip2/).

   ```python
   GEOIP_PATH = "path/to/GeoLite2-Country.mmdb"
   ```

## Usage

Once the above steps are completed, the middleware will restrict access to users from the whitelisted countries.

- **Example Usage with Middleware**: The middleware automatically restricts access for all views.

- **Restrict Access Per View**: You can also restrict access on a per-view basis using the `whitelisted_country_only` decorator:

   ```python
   from django.http import HttpResponse
   from nigerian_only.decorators import whitelisted_country_only

   @whitelisted_country_only
   def restricted_view(request):
       return HttpResponse("This is a restricted view to only whitelisted countries.")
   ```

## Important Notes

- **Access will not be restricted** if any of the steps mentioned above is not completed correctly.
- **Development Environment**: During development, the default IP address is `127.0.0.1`, which cannot determine the user's country. You need to set `WHITELISTED_IPS` in `settings.py` to allow access during development:

   ```python
   WHITELISTED_IPS = ['127.0.0.1']
   ```

- **Testing**: To test the middleware, use a VPN to change your location to one of the specified countries or use a valid IP address to determine the user's country.

## Example Project

You can check out this app with a basic setup example of the package here: [Django Nigeria Only Example](https://github.com/Afeez1131/django-nigerians-only-example).

## Contributing

Contributions are welcome and appreciated! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make changes and write tests to ensure your changes don't break anything.
4. Push the changes to your fork.
5. Submit a pull request.

## License

This project is licensed under the MIT License - see the `LICENSE` file for details.

## Developed by Afeez Lawal

### Contact Me:

- **Email**: [lawalafeez052@gmail.com](mailto:lawalafeez052@gmail.com)
- **LinkedIn**: [LinkedIn](https://www.linkedin.com/in/lawal-afeez/)
- **GitHub**: [GitHub](https://github.com/Afeez31)

---
