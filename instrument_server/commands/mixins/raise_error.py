from instrument_server.errors import CommandError


class RaiseErrorMixin:
    def raise_error(self, message):
        raise CommandError(f'{self.command}: {message}')
