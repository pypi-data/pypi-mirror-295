import setuptools

setuptools.setup(
    name="streamlit-msal-imperial-component",
    version="3.0.6",
    author="",
    author_email="",
    description="added view output",
    long_description="",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        # By definition, a Custom Component depends on Streamlit.
        # If your component has other Python dependencies, list
        # them here.
        "streamlit >= 1.36",
    ],
    extras_require={}
)
