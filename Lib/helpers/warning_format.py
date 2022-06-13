import warnings

def warn_format(message, category, filename, lineno, file=None, line=None):
	return '%s:%s: %s:%s\n' % (filename, lineno, category.__name__, message)

warnings.formatwarning = warn_format