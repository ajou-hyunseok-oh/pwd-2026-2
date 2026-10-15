"""Faithful English translations of the supplied source; no extra topics."""
TITLES={1:'Practical Web Service Development – Week 6',2:'Learning Objectives',3:'Servers and Node.js',4:'Web Service Structure',5:'The Role of a Server',6:'Comparison of Server Development Languages',7:'Node.js',8:'Node.js',9:'Core Concepts in Server Development',10:'HTTP/HTTPS',11:'HTTP Request Structure',12:'HTTP Response Structure',13:'JSON',14:'REST API',15:'Routing',16:'Middleware',17:'The MVC Pattern',18:'The MVCS Pattern',19:'The MVCS Pattern',20:'Test-Driven Development (TDD)',21:'Express Server App Development',22:'Express.js',23:'Creating an Express Project',24:'An Express MVCS Project',25:'Render',26:'Assignment Overview',27:'Q&A'}
TEXT={}
def add(page,text): TEXT[page]=text.strip().split('\n')
add(1,'''Web Server Development Using the Node.js Express Framework''')
add(2,'''Server development and Node.js
Node.js and
REST API design principles and implementation
Server architecture design (MVC / MVCS patterns)
TDD (Test Driven Development)''')
add(4,'''Client-server model: A structure for exchanging data through requests and responses between clients and servers
Client: A browser, mobile app, or another server
Server: Receives requests and returns appropriate responses
Network: The medium for transferring data between clients and servers (World Wide Web)
Protocols
HTTP/HTTPS: Rules for data communication between a web browser and a server. HTTPS adds SSL/TLS to HTTP to strengthen security.
REST: Representational State Transfer, an architectural style based on HTTP. RESTful services identify resources with URLs and manipulate them using HTTP requests (GET, POST, PUT, DELETE).
Data format
JSON (JavaScript Object Notation)''')
add(5,'''Receive client requests
Receive HTTP requests (URI, method, headers/body) and pass them to handlers according to routing rules
Process and compute data
Validate input, perform business logic, and execute computation or external API calls when needed
Communicate with a DB
Use CRUD queries to retrieve, store, update, and delete persistent data
Return processing results
Set status codes and headers, then serialize results as JSON, HTML, files, or other response formats
Authentication/authorization
Verify user identity (authentication) and check permissions to allow or deny resource access''')
add(6,'''By use case
Move quickly with one language for the frontend: Node.js
APIs connected to data/AI: Python
Finance/enterprise standards and complex domains: Java or .NET
Performance and simple deployment (single binary): Go
Sustained high performance and safety: Rust
Fast content, marketing, and back-office development: PHP / Ruby(Rails)
https://statisticsanddata.org/data/most-popular-backend-frameworks-2012-2025/''')
add(7,'''Node.js
Node.js is a JavaScript runtime environment built on Chrome's V8 JavaScript engine
A program that enables JavaScript to run outside a web browser
Features
1. JavaScript runtime
Run JavaScript on a computer without a browser
Develop server programs, desktop apps, and command-line tools
2. Asynchronous I/O (Non-blocking)
Handle multiple tasks concurrently
Proceed with other work without waiting for a task to finish
High performance and efficiency
3. Single-threaded event loop
Efficiently handle many connections with a single thread
Low memory usage
4. NPM ecosystem
The world's largest open-source library ecosystem
More than one million packages available''')
add(8,'''A JavaScript engine for writing high-performance asynchronous applications
An open-source project originally written by Ryan Dahl and first released on May 27, 2009 https://github.com/nodejs/node
A hybrid (interpreter + compiler) runtime using the V8 engine's JIT (Just-In-Time) compilation
V8 engine
Google's open-source JavaScript/WebAssembly engine written in C++
Execute JavaScript code quickly through a four-stage structure
Parsing → bytecode → JIT compilation → execution
Start immediately like an interpreter for fast initial response
Compile frequently used code to native code on the fly
Chrome/Edge (Chromium-based) browsers, Node.js
Chromium
An open-source web browser project led by Google https://blog.chromium.org/
Many recently released browsers are developed on Chromium''')
add(10,'''HTTP = HyperText Transfer Protocol
A protocol for exchanging hypertext quickly
Rules defining how a server and a client exchange messages
Process each HTTP request independently without linking or remembering information from previous requests (Stateless)
Send the necessary context with every request
Features
Scalability: Any server can handle any request.
Failure isolation: Sessions are not lost when one server goes down.
The same request yields the same result even when handled by another server
HTTPS = HyperText Transfer Protocol Secure
A protocol that strengthens security by encrypting data communication between a web browser and a website
Developed to address HTTP's vulnerability to hacking when transmitting data without encryption''')
add(12,'''Main status codes
2xx Success
200 OK
201 Created
4xx Client errors
400 Bad Request
404 Not Found
5xx Server errors
500 Server Error
503 Service Unavailable''')
add(13,'''JSON = JavaScript Object Notation
A data serialization format for exchanging data between servers and clients
Human-readable text
Easy for machines to parse
JSON rules
Six value types: string, number, boolean, null, object, array
Strings must use double quotes "..." (no single quotes)
No comments (neither // nor /* */)
No comma after the last element (no trailing comma)
JSON Online Validator and Formatter - JSON Lint (Do not use actual or production JSON data)
JaveScript JSON parsing and serialization''')
add(14,'''REST = REpresentational State Transfer
A resource-oriented architectural style based on HTTP
Develop by naming resources and exchanging their state
Components
Resource: HTTP URI
Action on a resource (Verb): HTTP Method
Content of an action on a resource (Representations): HTTP Message Pay Load
REST API
An API following REST principles
The goal is to design predictable, extensible APIs using standard HTTP
Design principles
URLs represent resources (not verbs, but nouns)
Express actions with methods
Stateless: Each request is independent
A consistent interface: A predictable structure''')
add(15,'''Connect requests received by a server to the handler functions that process them
Key format: Method (GET/POST/…), path (/users/:id)
The server framework builds and runs a routing table
Idempotency
GET, PUT, and DELETE must yield the same result even when executed multiple times
Prevent duplicate creations/payments despite timeouts or duplicate transmissions
Prevent duplicate processing in queue/retry environments (at-least-once delivery)
Idempotent requests can be safely cached and retransmitted
Make rollback/reprocessing easy (operations/failure response)''')
add(16,'''A block in the request-response pipeline that processes common logic up front to minimize a route's responsibilities
Benefits
Minimal responsibilities: A route only collects input → calls a service → responds.
Consistency: Centralize authentication/validation/error formats.
Reusability: Easily attach the same rules to multiple routes.
Testability: Unit-test common logic independently.
Security and quality: Apply basic safeguards such as Helmet, CORS, and Rate Limit globally.
Readability: Code reads like a "pipeline (flow)."''')
add(17,'''Model
The app's data structures and rules. Schemas, validation, DB access
View
Screens or data shown to users. Representations such as EJS/React/JSON
Controller
Receive requests, ask the Model to perform work, and respond with a View or JSON
Advantages
Role separation makes changes easy
Easy testing/reuse (service/model unit tests)
Reusability: The same controller logic can serve both EJS pages and a JSON API
Application
Server: Provide a JSON API through Model + Controller (+ Service)
Client (View): React (SPA) handles the screen''')
add(18,'''MVCS (Model–View–Controller–Service)
Add a Service layer to MVC to separate domain logic from the controller
Why is a Service necessary?
Prevent bloated controllers: Keep only request flow and move complex rules into services
Easy reuse/testing: Reuse the same rules across endpoints/jobs/webhooks; easy unit tests
Orchestrate multiple models/external APIs: Payments, notifications, transactions, caching, etc.
Consistent permissions/validation: Centralize rules such as "only the owner can edit"
Applying the MVCS pattern''')
add(19,'''Example application of the MVCS pattern''')
add(20,'''Test-driven development (TDD: Test-Driven Development)
Develop in short cycles: Write a test first, write the minimum code to pass it, then improve the code
Benefits
Catch bugs early: Failing tests expose issues before specifications become code
A refactoring safety net: Tests make structural changes safe
Design quality: Encourages small units (functions/layers) → a good fit with MVCS
Documentation: Tests become "executable example documentation"
CI/CD-friendly: Automatic verification on Git push (include tests in the pipeline)
TDD cycle: Red → Green → Refactor
Red: Define a state in which the feature does not work correctly
Green: Write the minimum working code to pass the test
Refactor: Improve code cleanliness and efficiency''')
add(22,'''A backend web application framework for building RESTful APIs with Node.js
Designed for building web applications and APIs
The de facto standard server framework for Node.js
Free, open-source software under the MIT license https://github.com/expressjs/express
Latest stable version 5.1.0 https://expressjs.com/
Plain Node.js
Express.js''')
add(23,'''Express execution test (Hello World)''')
add(24,'''Roles of each folder and main file
server.js: Server entry point - Load app.js, configure the port, and start the HTTP server with app.listen()
src/app.js: Express app configuration - Connect core middleware, routers, and error handlers
src/controllers: Receive requests, validate parameters → call services → format responses
src/data: Static data without code, such as initial dummy data, seed files, and JSON resources
src/middleware: Shared functions between requests and responses, such as authentication, logging, CORS, input validation, and error handling
src/models: Define DB schemas and data access logic (e.g. Mongoose Schema/Model, query methods)
src/routes: Express Router modules mapping URL paths and HTTP methods to controllers
src/services: Business logic layer - Combine multiple models/external APIs to implement domain rules
src/utils: Small reusable helper/utility functions''')
add(25,'''A PaaS (Platform-as-a-Service) cloud development platform that automatically builds and deploys code pushed to Git
One-click deployment and automatic redeployment
Service types
Web Service (long-running servers such as Express)
Static Site (static hosting)
Background Worker
Cron Job
Private Service.
Operational convenience
Environment variable management,
One free project, logs/health checks, and horizontal scaling support.''')
add(26,'''Ajou Campus Foodmap API with Express & Render
Learning objectives
Develop a REST API with Express
Learn the MVCS pattern
Learn asynchronous processing and error handling
Practice test-driven development
Required implementation
Is the project properly version-controlled in a GitHub repository?
Is the GitHub repository connected to Render for automatic deployment?
Do all server modules developed with Express work correctly?
Does the pwd-week3 React App receive data from the Render server?
Deadline
By September 28, 11:59
GitHub URL
(e.g. https://github.com/username/pwd-week4)
Render App URL
(e.g. https://pwd-week4-[username]..onrender.com)
Netlify App URL (Render server integration)
(e.g. https://pwd-week3-[username].netlify.app)''')
TABLES={
 6:[['Language','Frameworks','Advantages','Use cases'],['Node.js','Express, NestJS, Fastify','Fast I/O, full-stack JS','Real-time apps, API servers'],['Python','FastAPI, Django, Flask','Simple syntax, AI/ML','Data analysis, web apps'],['Java','Spring','Stability, large scale','Enterprise'],['PHP','Laravel','Web-focused, hosting','CMS, blogs']],
 11:[['Component','Description','Example'],['Method','Request type','GET, POST, PUT, DELETE'],['URL','Request path','/api/users'],['Headers','Additional information','Content-Type, Authorization'],['Body','Transmitted data','JSON, Form Data']],
 15:[['HTTP Method','CRUD','Description','Example'],['GET','Read','Retrieve resources','GET /users (all users)\nGET /users/1 (a specific user)'],['POST','Create','Create a resource','POST /users (create a user)'],['PUT','Update','Modify a resource','PUT /users/1 (update user information)'],['DELETE','Delete','Delete a resource','DELETE /users/1 (delete a user)']],
}
