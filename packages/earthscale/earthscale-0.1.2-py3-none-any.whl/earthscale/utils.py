def running_in_notebook() -> bool:
    try:
        from IPython import get_ipython  # type: ignore

        if get_ipython() is None:  # type: ignore
            return False
        return True
    except ImportError:
        return False
