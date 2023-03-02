Table of Contents

1.  Introduction

    1.  Purpose

    2.  Document Conventions

    3.  Intended Audience and Reading Suggestions

    4.  Project Scope

    5.  References

2.  Overall description

    1.  Product perspective

    2.  Product Features

    3.  User classes and Characteristics

    4.  Operating Environment

    5.  Design and Implementation Constraints

    6.  Assumptions and Dependencies

3.  System Features

    1.  Functional Requirements

4.  External Interface Requirements

    1.  User interfaces

    2.  Hardware interfaces

    3.  Software interfaces

    4.  Communication interfaces

5.  Nonfunctional Requirements

    1.  Performance Requirements

    2.  Safety Requirements

    3.  Security Requirements

    4.  Software Quality Attributes

```{=html}
<!-- -->
```
1.  **[Introduction]{.underline}**

    1.  [Purpose]{.underline}

> The purpose of this project is to build a web-application that provide
> easily accessible movies, serials, etc. and allow to add them to the
> personal lists.

2.  [Document Conventions]{.underline}

  -----------------------------------------------------------------------
  Shortage                            Description
  ----------------------------------- -----------------------------------
  HTML                                Hypertext Markup Language

  CSS                                 Cascading Style Sheets

  NF                                  Normal Form
  -----------------------------------------------------------------------

3.  [Intended Audience and Reading Suggestions]{.underline}

> This project is useful for the users to watch or read something, and
> mark them as watch by adding to their own lists.

4.  [Project Scope]{.underline}

> The purpose of the web-application to create a convenient and
> easy-to-use application for users, trying to watch or read something,
> or track all they are interested in. The system is based on a
> relational database.

2.  **[Overall description]{.underline}**

    1.  [Product perspective]{.underline}

> The product can store user ratings, and collect watching rating, that
> could be used in analytics.

2.  [Product Features]{.underline}

Major features of "Multilib" database shown below

![](SRS_Media/image1.png){width="7.086805555555555in"
height="2.8722222222222222in"}

3.  [User classes and Characteristics]{.underline}

> Users' functions.

-   Get all available products at web-site.

-   Be able to make a search request.

> Logged-in Users functions.

-   Get all available products at web-site.

-   Be able to make a search request.

-   Watch their lists.

> Administrative

-   Add/Delete/Update a product

    1.  [Operating Environment]{.underline}

> Operating environment for the web-site listed below.

-   Client/server architecture

-   Operating system: Windows/Linux

-   Database: MySQL

-   Platform: Python

-   Web-site: HTML+CSS

3.  **[System Features]{.underline}**

    1.  [Description and Priority]{.underline}

> The database contains such information about product, as title, year,
> country, genre, prehistory, poster and product. This product hasn't
> big priority, but still haven't good analogs.

2.  [Stimulus/Response sequences]{.underline}

-   Search the product you are looking for.

-   Get all information you required, or read/watch it.

    1.  [Functional Requirements]{.underline}

> Client/Server Architecture
>
> The term client/server architecture refers primarily to an
> architecture or logical division of responsibilities, the client is
> the web-application (also known as the front-end), and the server
> (also known as the back-end).
>
> A client/server system is a distributed system in which, some sites
> are client sites and others are server sites.
>
> All the data resides at the server sites.
>
> All applications execute at the client sites.

4.  **[External Interface Requirements]{.underline}**

    1.  [User interfaces]{.underline}

> Front-end software: HTML & CSS
>
> Back-end software: Python, Flask, MySQL

2.  [Hardware interfaces]{.underline}

> Ubuntu
>
> A browser which supports HTML & JavaScript

3.  [Software interfaces]{.underline}

> Ubuntu: for good performance
>
> Database: to save films, books, etc. and users lists

4.  [Communication interfaces]{.underline}

> This project supports all types of web browsers. We are using simple
> electronic forms for the project.

5.  **[Nonfunctional Requirements]{.underline}**

    1.  [Performance Requirements]{.underline}

> The steps involved to perform the implementation of web-library
> database are listed below.
>
> Normalization:
>
> The basic objective of normalization is to reduce redundancy which
> means that information is to be stored only once. Storing information
> several times leads to wastage of storage space and increase in the
> total size of the data stored. If a database is not properly designed
> it can give rise to modification anomalies. Modification anomalies
> arise when data is added to, changed or deleted from a database table.
> Similarly, in traditional databases as well as improperly designed
> relational databases, data redundancy can be a problem. These can be
> eliminated by normalizing a database. Normalization is the process of
> breaking down a table into smaller tables. So that each table deals
> with a single theme. There are three different kinds of modifications
> of anomalies and formulated the first, second and third normal forms
> (3NF) is considered sufficient for most practical purposes. It should
> be considered only after a thorough analysis and complete
> understanding of its implications.

2.  [Safety Requirements]{.underline}

> If there is extensive damage to a wide portion of the database due to
> catastrophic failure, such as a disk crash, the recovery method
> restores a past copy of the database that was backed up to archival
> storage and reconstruct database.

3.  [Security Requirements]{.underline}

> Security systems need database storage just like many other
> applications.

4.  [Software Quality Attributes]{.underline}

> Availability: The web-site should be available anytime, for every one
> user.
>
> Correctness: Web-site should find products even if user entered only
> half of the product name.
>
> Maintainability: The administrators should moderate users, and add new
> products.
>
> Usability: Web-site should satisfy a maximum number of users and their
> needs.
