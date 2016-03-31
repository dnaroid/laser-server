Create a backend for simple News Management application using all knowledge from 
Training. Pay attention that your application should be without view layer (UI).

Your application should perform next operations:
+ Add news;
- Edit news;
- Delete news;
+ View the list of news;
- View single news message;
- Add news author;
+ Search according SearchCtiteria (see details in Implementation requirements section);
- Add tag/tags for news message;
- Add comment(s) for news message;
- Delete comment(s);
- Get list of news messages should be sorted by most commented news.
- Save news message with author and tags should go as one step in service layer;
- Each news should have only one author;
- Each news may  have more than 1 tag;
- Count all news;

Implementation requirements:
- Persistence layers should implement four basic C.R.U.D operations.
- Sun java coding conventions;
- Follow naming standards for all database objects;
- Use Spring Dependency  Injection and Inversion of Control;
- Service layer should be tested using mocking framework - Mockito;
- Persistence layer should be tested using DBUnit framework. Default data for testing should be loaded automatically.
- Use Transfer Object to represent each database entity.
- For search functionality use SeachCriteria object which may contains: author entity and list of tags (will be using for constructing SQL queries in DAO layer);
- Note: author can be deleted – it’s possible to make him expired (not displayable in author dropdown, but visible on news list and view/update news);

System requirements:
• Database: Oracle (version 10 and higher)
• Data access: JDBC (simple SQL);
• Use bitbucket as code repository.

Definition of done:
- Code is clean, readable and documented;
- The application should has correct structure of packages; 
- Database schema should be adjusted as described on page 2. Create 2 separate db scripts: one for db schema generation and one for loading default data (near 20 items for each table);
- Exception handling;
- Logging;
- Application should be built using Maven in jar file (preferable to do it manually using command line, without help of IDE);

