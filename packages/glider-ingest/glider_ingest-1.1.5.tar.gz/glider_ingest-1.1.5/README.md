<a id="readme-top"></a>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/alecmkrueger/glider-ingest">
    <img src="https://github.com/alecmkrueger/project_images/blob/main/TAMU-GERG-Glider.jpg?raw=true" alt="Logo" width="500" height="272">
  </a>

<h3 align="center">GERG Glider Ingest</h3>

  <p align="center">
    Convert raw data from GERG gliders into netcdf using python
    <br />
    <a href="https://github.com/alecmkrueger/glider-ingest"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/alecmkrueger/glider-ingest/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/alecmkrueger/glider-ingest/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#dependencies">Dependencies</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project was created to streamline the process of converting the raw data from the gliders after missions into NetCDF files, 
as well as ensuring the code can be easily maintained, understood, and used by others.



### Built With

[![Python][Python]][Python-url]



<!-- GETTING STARTED -->
## Getting Started

Using PyPi
```sh
pip install glider-ingest
```

### Dependencies

Required dependencies are:
* python = "^3.12"
* numpy = "^2.0.1"
* pandas = "^2.2.2"
* xarray = "^2024.6.0"
* attrs = "^23.2.0"
* gsw = "^3.6.19"
* scipy = "^1.14.0"
* netcdf4 = "^1.7.1.post1"


<!-- USAGE EXAMPLES -->
## Usage

Process raw data from gliders using python.

Example:

```sh
from glider_ingest.ingest import process

ds = process(glider_number = 'Glider_Number',
             mission_title = 'Mission_Title',
             extensions = ['DBD','EBD'],
             raw_data_source = 'path/to/raw_data',
             working_directory = 'path/to/working_directory',
             output_nc_filename = 'Mission_Title_Glider_Number.nc',
             return_ds = True)
```


<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Alec Krueger - alecmkrueger@tamu.edu

Project Link: [https://github.com/alecmkrueger/glider-ingest](https://github.com/alecmkrueger/glider-ingest)



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* Sakib Mahmud, Texas A&M University, Geochemical and Environmental Research Group, sakib@tamu.edu
* Xiao Ge, Texas A&M University, Geochemical and Environmental Research Group, gexiao@tamu.edu
* Alec Krueger, Texas A&M University, Geochemical and Environmental Research Group, alecmkrueger@tamu.edu

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/alecmkrueger/glider-ingest.svg?style=for-the-badge
[contributors-url]: https://github.com/alecmkrueger/glider-ingest/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/alecmkrueger/glider-ingest.svg?style=for-the-badge
[forks-url]: https://github.com/alecmkrueger/glider-ingest/network/members
[stars-shield]: https://img.shields.io/github/stars/alecmkrueger/glider-ingest.svg?style=for-the-badge
[stars-url]: https://github.com/alecmkrueger/glider-ingest/stargazers
[issues-shield]: https://img.shields.io/github/issues/alecmkrueger/glider-ingest.svg?style=for-the-badge
[issues-url]: https://github.com/alecmkrueger/glider-ingest/issues
[license-shield]: https://img.shields.io/github/license/alecmkrueger/glider-ingest.svg?style=for-the-badge
[license-url]: https://github.com/alecmkrueger/glider-ingest/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/aleckrueger
[Python]: https://img.shields.io/badge/python-000000?&logo=python
[Python-url]: https://www.python.org/