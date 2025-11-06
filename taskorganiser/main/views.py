from django.shortcuts import render


def dashboard_view(request):
	"""Render the main dashboard page if present, otherwise show a placeholder."""
	context = {
		'BOARD': {'name': 'My Board'}
	}
	# If the dashboard template exists, render it; otherwise render a simple placeholder
	try:
		return render(request, 'dashboard/main.html', context)
	except Exception:
		return render(request, 'home.html', context)


def home_view(request):
	"""Render the standalone home.html template."""
	return render(request, 'home.html')
