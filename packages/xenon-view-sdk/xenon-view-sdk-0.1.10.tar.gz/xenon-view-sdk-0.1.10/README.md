# xenon-view-sdk
The Xenon View Python SDK is the Python SDK to interact with [XenonView](https://xenonview.com).

**Table of contents:** <a id='contents'></a>

* [What's New](#whats-new)
* [Introduction](#intro)
* [Steps To Get Started](#getting-started)
    * [Identify Business Outcomes](#step-1)
    * [Identify Customer Journey Milestones](#step-2)
    * [Enumerate Technical Stack](#step-3)
    * [Installation](#step-4)
    * [Instrument Business Outcomes](#step-5)
    * [Instrument Customer Journey Milestones](#step-6)
    * [Determine Commit Points](#step-7)
    * [(Optional) Group Customer Journeys](#step-8)
    * [Analysis](#step-9)
    * [Perform Experiments](#step-10)
* [Detailed Usage](#detailed-usage)
    * [Installation](#installation)
    * [Initialization](#instantiation)
    * [Service/Subscription/SaaS Business Outcomes](#saas)
    * [Ecommerce Business Outcomes](#ecom)
    * [Customer Journey Milestones](#milestones)
        * [Features Usage](#feature-usage)
        * [Content Interaction](#content-interaction)
    * [Commit Points](#commiting)
    * [Heartbeats](#heartbeat)
    * [Platforming](#platforming)
    * [Experiments](#experiments)
    * [Customer Journey Grouping](#deanonymizing-journeys)
    * [Other Considerations](#other)
        * [(Optional) Error Handling](#errors)
        * [(Optional) Custom Customer Journey Milestones](#custom)
        * [(Optional) Journey Identification](#cuuid)
        * [(Optional) Augment Calls with URL](#augment-calls)
* [License](#license)

<br/>

## What's New <a id='whats-new'></a>
* v0.1.10 - method for adding url to every event
* v0.1.9 - Added: Abandonment Watchdog Feature, leadAttribution outcome
* v0.1.8 - Added: Term for all subscriptions.
* v0.1.7 - Added: changed value to price.
* v0.1.6 - Added: Downsell, Ad, Content Archive, Subscription Pause and included price for all subscriptions
* v0.1.5 - remove journeys call 
* v0.1.4 - Rename tag to variant
* v0.1.3 - Readme update
* v0.1.2 - typo fixed
* v0.1.1 - duplicates for new SDK handled
* v0.1.0 - SDK redesign

<br/>


## Introduction <a id='intro'></a>
Everyone should have access to world-class customer telemetry.

You should be able to identify the most pressing problems affecting your business quickly.
You should be able to determine if messaging or pricing, or technical challenges are causing friction for your customers.
You should be able to answer questions like:
1. Is my paywall wording or the price of my subscriptions causing my customers to subscribe less?
2. Is my website performance or my application performance driving retention?
3. Is purchasing a specific product or the product portfolio driving referrals?

With the correct approach to instrumentation coupled with AI-enhanced analytics, you can quickly answer these questions and much more.

<br/>

[back to top](#contents)

## Get Started With The Following Steps: <a id='getting-started'></a>
The Xenon View SDK can be used in your application to provide a new level of customer telemetry. You'll need to embed the instrumentation into your website/application via this SDK.

Instrumentation will vary based on your use case; are you offering a service/subscription (SaaS) or selling products (Ecom)?

In a nutshell, the steps to get started are as follows:
1. Identify Business Outcomes and Customer Journey Milestones leading to those Outcomes.
2. Instrument the Outcomes/Milestones.
3. Analyze the results.

<br/>


### Step 1 - Business Outcomes <a id='step-1'></a>

Regardless of your business model, your first step will be identifying your desired business outcomes.

**Example - Service/Subscription/SaaS**:
1. Lead Capture
2. Account Signup
3. Initial Subscription
4. Renewed Subscription
5. Upsold Subscription
6. Referral

**Example - Ecom**:
1. Place the product in the cart
2. Checkout
3. Upsold
4. Purchase

> :memo: Note: Each outcome has an associated success and failure.

<br/>


### Step 2 - Customer Journey Milestones <a id='step-2'></a>

For each Business Outcome, identify potential customer journey milestones leading up to that business outcome.

**Example - Service/Subscription/SaaS for _Lead Capture_**:
1. View informational content
2. Asks question in the forum
3. Views FAQs
4. Views HowTo
5. Requests info product

**Example - Ecom for _Place product in cart_** :
1. Search for product information
2. Learns about product
3. Read reviews

<br/>

### Step 3 - Enumerate Technical Stack <a id='step-3'></a>

Next, you will want to figure out which SDK to use. We have some of the most popular languages covered.

Start by listing the technologies involved and what languages your company uses. For example:
1. Front end - UI (Javascript - react)
2. Back end - API server (Java)
3. Mobile app - iPhone (Swift)
4. Mobile app - Android (Android Java)

Next, figure out how your outcomes spread across those technologies. Below are pointers to our currently supported languages:
* [React](https://github.com/xenonview-com/view-js-sdk)
* [Next.Js](https://github.com/xenonview-com/view-js-sdk)
* [Angular](https://github.com/xenonview-com/view-js-sdk)
* [HTML](https://github.com/xenonview-com/view-js-sdk)
* [Plain JavaScript](https://github.com/xenonview-com/view-js-sdk)
* [iPhone/iPad](https://github.com/xenonview-com/view-swift-sdk)
* [Mac](https://github.com/xenonview-com/view-swift-sdk)
* [Java](https://github.com/xenonview-com/view-java-sdk)
* [Android Java](https://github.com/xenonview-com/view-java-sdk)
* [Python](https://github.com/xenonview-com/view-python-sdk)

Finally, continue the steps below for each technology and outcome.


### Step 4 - Installation <a id='step-4'></a>

After you have done the prework of [Step 1](#step-1) and [Step 2](#step-2), you are ready to [install Xenon View](#installation).
Once installed, you'll need to [initialize the SDK](#instantiation) and get started instrumenting.


<br/>
<br/>


### Step 5 - Instrument Business Outcomes <a id='step-5'></a>

We have provided several SDK calls to shortcut your instrumentation and map to the outcomes identified in [Step 1](#step-1).  
These calls will roll up into the associated Categories during analysis. These rollups allow you to view each Category in totality.
As you view the categories, you can quickly identify issues (for example, if there are more Failures than Successes for a Category).

**[Service/Subscription/SaaS Related Outcome Calls](#saas)**  (click on a call to see usage)

| Category                 | Success                                               | Decline                                                                                                                    |
|--------------------------|-------------------------------------------------------|----------------------------------------------------------------------------------------------------------------------------|
| Lead Attribution         | [`leadAttribution()`](#saas-lead-attribution)         |                                                                                                                            |
| Lead Capture             | [`leadCaptured()`](#saas-lead-capture)                | [`leadCaptureDeclined()`](#saas-lead-capture-fail)                                                                         |
| Account Signup           | [`accountSignup()`](#saas-account-signup)             | [`accountSignupDeclined()`](#saas-account-signup-fail)                                                                     |
| Application Installation | [`applicationInstalled()`](#saas-application-install) | [`applicationNotInstalled()`](#saas-application-install-fail)                                                              |
| Initial Subscription     | [`initialSubscription()`](#saas-initial-subscription) | [`subscriptionDeclined()`](#saas-initial-subscription-fail)                                                                |
| Subscription Renewed     | [`subscriptionRenewed()`](#saas-renewed-subscription) | [`subscriptionCanceled()`](#saas-renewed-subscription-fail) / [`subscriptionPaused()`](#saas-paused-subscription)          |
| Subscription Upsell      | [`subscriptionUpsold()`](#saas-upsell-subscription)   | [`subscriptionUpsellDeclined()`](#saas-upsell-subscription-fail) / [`subscriptionDownsell()`](#saas-downsell-subscription) |
| Ad Clicked               | [`adClicked()`](#saas-ad-clicked)                     | [`adIgnored()`](#saas-ad-ignored)                                                                                          |
| Referral                 | [`referral()`](#saas-referral)                        | [`referralDeclined()`](#saas-referral-fail)                                                                                |


**[Ecom Related Outcome Calls](#ecom)** (click on a call to see usage)

| Category            | Success                                           | Decline                                                                                   |
|---------------------|---------------------------------------------------|-------------------------------------------------------------------------------------------|
| Lead Attribution    | [`leadAttribution()`](#ecom-lead-attribution)     |                                                                                           |
| Lead Capture        | [`leadCaptured()`](#ecom-lead-capture)            | [`leadCaptureDeclined()`](#ecom-lead-capture-fail)                                        | 
| Account Signup      | [`accountSignup()`](#ecom-account-signup)         | [`accountSignupDeclined()`](#ecom-account-signup-fail)                                    | 
| Add To Cart         | [`productAddedToCart()`](#ecom-product-to-cart)   | [`productNotAddedToCart()`](#ecom-product-to-cart-fail)                                   |
| Product Upsell      | [`upsold()`](#ecom-upsell)                        | [`upsellDismissed()`](#ecom-upsell-fail)                                                  | 
| Checkout            | [`checkedOut()`](#ecom-checkout)                  | [`checkoutCanceled()`](#ecom-checkout-fail) / [`productRemoved()`](#ecom-checkout-remove) | 
| Purchase            | [`purchased()`](#ecom-purchase)                   | [`purchaseCanceled()`](#ecom-purchase-fail)                                               | 
| Promise Fulfillment | [`promiseFulfilled()`](#ecom-promise-fulfillment) | [`promiseUnfulfilled()`](#ecom-promise-fulfillment-fail)                                  | 
| Product Disposition | [`productKept()`](#ecom-product-outcome)          | [`productReturned()`](#ecom-product-outcome-fail)                                         |
| Referral            | [`referral()`](#ecom-referral)                    | [`referralDeclined()`](#ecom-referral-fail)                                               |

<br/>

### Step 6 - Instrument Customer Journey Milestones <a id='step-6'></a>

Next, you will want to instrument your website/application/backend/service for the identified Customer Journey Milestones [Step 2](#step-2).
We have provided several SDK calls to shortcut your instrumentation here as well.  

During analysis, each Milestone is chained together with the proceeding and following Milestones.
That chain terminates with an Outcome (described in [Step 4](#step-4)).
AI/ML is employed to determine Outcome correlation and predictability for the chains and individual Milestones.
During the [analysis step](#step-8), you can view the correlation and predictability as well as the Milestone chains
(called Customer Journeys in this guide).

Milestones break down into two types (click on a call to see usage):

| Features | Content |
| --- | --- |
| [`featureAttempted()`](#feature-started) | [`contentViewed()`](#content-viewed) |
| [`featureFailed()`](#feature-failed) | [`contentCreated()`](#content-created) / [`contentEdited()`](#content-edited) |
| [`featureCompleted()`](#feature-complete) |  [`contentDeleted()`](#content-deleted) / [`contentArchived()`](#content-archived) |
| | [`contentRequested()`](#content-requested)/[`contentSearched()`](#content-searched)|

<br/>

### Step 7 - Commit Points <a id='step-7'></a>


Once instrumented, you'll want to select appropriate [commit points](#commit). Committing will initiate the analysis on your behalf by Xenon View.

<br/>
<br/>

### Step 8 (Optional) - Group Customer Journeys <a id='step-8'></a>

All the customer journeys (milestones and outcomes) are anonymous by default.
For example, if a Customer interacts with your brand in the following way:
1. Starts on your marketing website.
2. Downloads and uses an app.
3. Uses a feature requiring an API call.


*Each of those journeys will be unconnected and not grouped.*

To associate those journeys with each other, you can [deanonymize](#deanonymizing-journeys) the Customer. Deanonymizing will allow for a deeper analysis of a particular user.

Deanonymizing is optional. Basic matching of the customer journey with outcomes is valuable by itself. Deanonymizing will add increased insight as it connects Customer Journeys across devices.

<br/>

### Step 9 - Analysis <a id='step-9'></a>


Once you have released your instrumented code, you can head to [XenonView](https://xenonview.com/) to view the analytics.

<br/>

### Step 10 - Perform Experiments <a id='step-10'></a>

There are multiple ways you can experiment using XenonView. We"ll focus here on three of the most common: time, platform, and variant based cohorts.

#### Time-based cohorts
Each Outcome and Milestone is timestamped. You can use this during the analysis phase to compare timeframes. A typical example is making a feature change.
Knowing when the feature went to production, you can filter in the XenonView UI based on the timeframe before and the timeframe after to observe the results.

#### Variant-based cohorts
You can identify a journey collection as an [experiment](#experiments) before collecting data. This will allow you to run A/B testing-type experiments (of course not limited to two).
As an example, let"s say you have two alternate content/feature variants and you have a way to direct half of the users to Variant A and the other half to Variant B.
You can name each variant before the section of code that performs that journey. After collecting the data, you can filter in the XenonView UI based on each variant to
observe the results.

#### Platform-based cohorts
You can [Platform](#platforming) any journey collection before collecting data. This will allow you to experiment against different platforms:
* Operating System Name
* Operating System version
* Device model (Pixel, iPhone 14, Docker Container, Linux VM, Dell Server, etc.)
* A software version of your application.

As an example, let's say you have an iPhone and Android mobile application and you want to see if an outcome is more successful on one device verse the other.
You can platform before the section of code that performs that flow. After collecting the data, you can filter in the XenonView UI based on each platform to
observe the results.

<br/>
<br/>
<br/>

[back to top](#contents)

## Detailed Usage <a id='detailed-usage'></a>
The following section gives detailed usage instructions and descriptions.
It provides code examples for each of the calls.

The SDK supports Python 3+.

<br/>

### Installation <a id='installation'></a>

You can install the View Python SDK from [PyPI](https://pypi.org/project/xenon-view-sdk):

```bash
    pip install xenon-view-sdk
```

<br/>

[back to top](#contents)

### Instantiation <a id='instantiation'></a>

The View SDK is a Python module you'll need to include in your application. After inclusion, you'll need to init the singleton object:


```python
from xenon_view_sdk import Xenon

# start by initializing Xenon View
Xenon('<API KEY>')
```

-OR-

```python
from xenon_view_sdk import Xenon

# to initialize Xenon View after construction
Xenon('TBD')
Xenon().key('<API KEY>')
```

Of course, you'll have to make the following modifications to the above code:
- Replace `<API KEY>` with your [api key](https://xenonview.com/api-get)

<br/>

[back to top](#contents)

### Service/Subscription/SaaS Related Business Outcomes <a id='saas'></a>
<br/>

#### Lead Attributed  <a id='saas-lead-attributed'></a>
Use this call to track Lead Attribution (Google Ads, Facebook Ads, etc.)
You can add a source and identifier string to the call to differentiate as follows:

<br/>

##### ```leadAttributed()```

```python
from xenon_view_sdk import Xenon

source = 'Google Ad'
identifier = 'Search'

# Successful Lead Attributed to Google Ad
Xenon().leadAttributed(source)
#...
# Successful Lead Attributed to Google Search Ad
Xenon().leadAttributed(source, identifier)
```

<br/>

#### Lead Capture  <a id='saas-lead-capture'></a>
Use this call to track Lead Capture (emails, phone numbers, etc.)
You can add a specifier string to the call to differentiate as follows:

<br/>

##### ```leadCaptured()```
```python
from xenon_view_sdk import Xenon

emailSpecified = "Email"
phoneSpecified = "Phone Number"

# Successful Lead Capture of an email
Xenon().leadCaptured(emailSpecified)
# ...
# Successful Lead Capture of a phone number
Xenon().leadCaptured(phoneSpecified)
```
<br/>

##### ```leadCaptureDeclined()``` <a id='saas-lead-capture-fail'></a>
> :memo: Note: You want to be consistent between success and failure and match the specifiers
```python
from xenon_view_sdk import Xenon

emailSpecified = "Email"
phoneSpecified = "Phone Number" 

# Unsuccessful Lead Capture of an email
Xenon().leadCaptureDeclined(emailSpecified)
# ...
# Unsuccessful Lead Capture of a phone number
Xenon().leadCaptureDeclined(phoneSpecified)
```

<br/>

#### Account Signup  <a id='saas-account-signup'></a>
Use this call to track when customers signup for an account.
You can add a specifier string to the call to differentiate as follows:

<br/>

##### ```accountSignup()```
```python
from xenon_view_sdk import Xenon

viaFacebook = "Facebook"
viaGoogle = "Google"
viaEmail = "Email"

# Successful Account Signup with Facebook
Xenon().accountSignup(viaFacebook)
# ...
# Successful Account Signup with Google
Xenon().accountSignup(viaGoogle)
# ...
# Successful Account Signup with an Email
Xenon().accountSignup(viaEmail)
```

<br/>

##### ```accountSignupDeclined()``` <a id='saas-account-signup-fail'></a>
> :memo: Note: You want to be consistent between success and failure and match the specifiers
```python
from xenon_view_sdk import Xenon

viaFacebook = "Facebook"
viaGoogle = "Google"
viaEmail = "Email"

# Unsuccessful Account Signup with Facebook
Xenon().accountSignupDeclined(viaFacebook)
# ...
# Unsuccessful Account Signup with Google
Xenon().accountSignupDeclined(viaGoogle)
# ...
# Unsuccessful Account Signup with an Email
Xenon().accountSignupDeclined(viaEmail)
```

<br/>

#### Application Installation  <a id='saas-application-install'></a>
Use this call to track when customers install your application.

<br/>

##### ```applicationInstalled()```
```python
from xenon_view_sdk import Xenon

# Successful Application Installation
Xenon().applicationInstalled()
```

<br/>

##### ```applicationNotInstalled()``` <a id='saas-application-install-fail'></a>
> :memo: Note: You want consistency between success and failure.
```python
from xenon_view_sdk import Xenon

# Unsuccessful or not completed Application Installation
Xenon().applicationNotInstalled()
```

<br/>

#### Initial Subscription  <a id='saas-initial-subscription'></a>
Use this call to track when customers initially subscribe.
You can add a specifier string to the call to differentiate as follows:

<br/>

##### ```initialSubscription()```
```python
from xenon_view_sdk import Xenon

tierSilver = "Silver Monthly"
tierGold = "Gold"
tierPlatium = "Platium"
annualSilver = "Silver Annual"
method = "Stripe" # optional
price = '$25' #optional
term = "30d" #optional

# Successful subscription of the lowest tier with Stripe
Xenon().initialSubscription(tierSilver, method)

# Successful subscription of the lowest tier with Stripe for $25 for term
Xenon().initialSubscription(tierSilver, method, price, term)
# ...
# Successful subscription to the middle tier
Xenon().initialSubscription(tierGold)
# ...
# Successful subscription to the top tier
Xenon().initialSubscription(tierPlatium)
# ...
# Successful subscription of an annual period
Xenon().initialSubscription(annualSilver)
```

<br/>

##### ```subscriptionDeclined()``` <a id='saas-initial-subscription-fail'></a>
> :memo: Note: You want to be consistent between success and failure and match the specifiers
```python
from xenon_view_sdk import Xenon

tierSilver = "Silver Monthly"
tierGold = "Gold"
tierPlatium = "Platium"
annualSilver = "Silver Annual"
method = "Stripe" # optional
price = '$25' # optional
term = "30d" # optional

# Unsuccessful subscription of the lowest tier
Xenon().subscriptionDeclined(tierSilver)
# ...
# Unsuccessful subscription of the middle tier
Xenon().subscriptionDeclined(tierGold)
# ...
# Unsuccessful subscription to the top tier
Xenon().subscriptionDeclined(tierPlatium)
# ...
# Unsuccessful subscription of an annual period with Stripe
Xenon().subscriptionDeclined(annualSilver, method)

# Unsuccessful subscription of an annual period for $25 for term
Xenon().subscriptionDeclined(annualSilver, method, price, term)
```

<br/>

#### Subscription Renewal  <a id='saas-renewed-subscription'></a>
Use this call to track when customers renew.
You can add a specifier string to the call to differentiate as follows:

<br/>

##### ```subscriptionRenewed()```
```python
from xenon_view_sdk import Xenon

tierSilver = "Silver Monthly"
tierGold = "Gold"
tierPlatium = "Platium"
annualSilver = "Silver Annual"
method = "Stripe" #optional
price = '$25' # optional
term = "30d" #optional

# Successful renewal of the lowest tier with Stripe
Xenon().subscriptionRenewed(tierSilver, method)

# Successful renewal of the lowest tier with Stripe for $25 for term
Xenon().subscriptionRenewed(annualSilver, method, price, term)
# ...
# Successful renewal of the middle tier
Xenon().subscriptionRenewed(tierGold)
# ...
# Successful renewal of the top tier
Xenon().subscriptionRenewed(tierPlatium)
# ...
# Successful renewal of an annual period
Xenon().subscriptionRenewed(annualSilver)
```

<br/>

##### ```subscriptionCanceled()``` <a id='saas-renewed-subscription-fail'></a>
> :memo: Note: You want to be consistent between success and failure and match the specifiers
```python
from xenon_view_sdk import Xenon

tierSilver = "Silver Monthly"
tierGold = "Gold"
tierPlatium = "Platium"
annualSilver = "Silver Annual"
method = "Stripe" #optional
price = '$25' # optional
term = "30d" #optional

# Canceled subscription of the lowest tier
Xenon().subscriptionCanceled(tierSilver)
# ...
# Canceled subscription of the middle tier
Xenon().subscriptionCanceled(tierGold)
# ...
# Canceled subscription of the top tier
Xenon().subscriptionCanceled(tierPlatium)
# ...
# Canceled subscription of an annual period with Stripe
Xenon().subscriptionCanceled(annualSilver, method)

# Canceled subscription of an annual period with Stripe for $25
Xenon().subscriptionCanceled(annualSilver, method, price, term)
```
<br/>

##### ```subscriptionPaused()``` <a id='saas-paused-subscription'></a>

> :memo: Note: You want to be consistent between success and failure and match the specifiers
```python
from xenon_view_sdk import Xenon

tierSilver = "Silver Monthly"
tierGold = "Gold"
tierPlatium = "Platium"
annualSilver = "Silver Annual"
method = "Stripe" #optional
price = '$25' # optional
term = "30d" #optional

# Paused subscription of the lowest tier
Xenon().subscriptionPaused(tierSilver)
# ...
# Paused subscription of the middle tier
Xenon().subscriptionPaused(tierGold)
# ...
# Paused subscription of the top tier
Xenon().subscriptionPaused(tierPlatium)
# ...
# Paused subscription of an annual period with Stripe
Xenon().subscriptionPaused(annualSilver, method)

# Paused subscription of an annual period with Stripe for $25 for term
Xenon().subscriptionPaused(annualSilver, method, price, term)
```

<br/>

#### Subscription Upsold  <a id='saas-upsell-subscription'></a>
Use this call to track when a Customer upgrades their subscription.  
You can add a specifier string to the call to differentiate as follows:

<br/>

##### ```subscriptionUpsold()```
```python
from xenon_view_sdk import Xenon

tierGold = "Gold Monthly"
tierPlatium = "Platium"
annualGold = "Gold Annual"
method = "Stripe" #optional
price = '$25' # optional
term = "30d" #optional

# Assume already subscribed to Silver

# Successful upsell of the middle tier with Stripe
Xenon().subscriptionUpsold(tierGold, method)

# Successful upsell of the middle tier with Stripe for $25 for term
Xenon().subscriptionUpsold(tierGold, method, price, term)
# ...
# Successful upsell of the top tier
Xenon().subscriptionUpsold(tierPlatium)
# ...
# Successful upsell of middle tier - annual period
Xenon().subscriptionUpsold(annualGold)
```

<br/>

##### ```subscriptionUpsellDeclined()``` <a id='saas-upsell-subscription-fail'></a>
> :memo: Note: You want to be consistent between success and failure and match the specifiers
```python
from xenon_view_sdk import Xenon

tierGold = "Gold Monthly"
tierPlatium = "Platium"
annualGold = "Gold Annual"
method = "Stripe" #optional
price = '$25' # optional
term = "30d" #optional

# Assume already subscribed to Silver

# Rejected upsell of the middle tier
Xenon().subscriptionUpsellDeclined(tierGold)
# ...
# Rejected upsell of the top tier
Xenon().subscriptionUpsellDeclined(tierPlatium)
# ...
# Rejected upsell of middle tier - annual period
Xenon().subscriptionUpsellDeclined(annualGold, method)

# Rejected upsell of middle tier - annual period with Stripe for $25 for term
Xenon().subscriptionUpsellDeclined(annualGold, method, price, term)
```
<br/>

##### ```subscriptionDownsell()``` <a id='saas-downsell-subscription'></a>
> :memo: Note: You want to be consistent between success and failure and match the specifiers
```python
from xenon_view_sdk import Xenon

tierGold = "Gold Monthly"
tierPlatium = "Platium"
annualGold = "Gold Annual"
method = "Stripe" #optional
price = '$15' #optional
term = "30d" #optional

# Assume already subscribed to Platium

# Downsell to Gold
Xenon().subscriptionDownsell(tierGold)
# ...
# Downsell to Gold annual with method
Xenon().subscriptionDownsell(annualGold, method)

# Downsell to Gold - annual period with Stripe for $15 for term
Xenon().subscriptionDownsell(annualGold, method, price, term)
```

<br/>

#### Ad Clicked  <a id='saas-ad-clicked'></a>
Use this call to track when customers click on an Advertisement.
You can add a specifier string to the call to differentiate as follows:

<br/>

##### ```adClicked()```
```python
from xenon_view_sdk import Xenon

provider = "AdMob"
id = "ID-1234" # optional
price = "$0.25" # optional

# Click an Ad from AdMob
Xenon().adClicked(provider)
# ...
# Click an Ad from AdMob identfied by ID-1234
Xenon().adClicked(provider, id)
# ...
# Click an Ad from AdMob identfied by ID-1234 with price 
Xenon().adClicked(provider, id, price)
```

<br/>


##### ```adIgnored()```  <a id='saas-ad-ignored'></a>
```python
from xenon_view_sdk import Xenon

provider = "AdMob"
id = "ID-1234" # optional
price = "$0.25" # optional

# No action on an Ad from AdMob
Xenon().adIgnored(provider)
# ...
# No action on an Ad from AdMob identfied by ID-1234
Xenon().adIgnored(provider, id)
# ...
# No action on an Ad from AdMob identfied by ID-1234 with price 
Xenon().adIgnored(provider, id, price)
```

<br/>


#### Referral  <a id='saas-referral'></a>
Use this call to track when customers refer someone to your offering.
You can add a specifier string to the call to differentiate as follows:

<br/>

##### ```referral()```
```python
from xenon_view_sdk import Xenon

kind = "Share"
detail = "Review" #optional

# Successful referral by sharing a review
Xenon().referral(kind, detail)
# -OR-
Xenon().referral(kind)
```

<br/>

##### ```referralDeclined()``` <a id='saas-referral-fail'></a>
> :memo: Note: You want to be consistent between success and failure and match the specifiers
```python
from xenon_view_sdk import Xenon

kind = "Share"
detail = "Review" #optional

# Customer declined referral 
Xenon().referralDeclined(kind, detail)
# -OR-
Xenon().referralDeclined(kind)
```

<br/>

[back to top](#contents)

### Ecommerce Related Outcomes <a id='ecom'></a>

<br/>

#### Lead Attributed  <a id='ecom-lead-attributed'></a>
Use this call to track Lead Attribution (Google Ads, Facebook Ads, etc.)
You can add a source and identifier string to the call to differentiate as follows:

<br/>

##### ```leadAttributed()```

```python
from xenon_view_sdk import Xenon

source = 'Google Ad'
identifier = 'Search'

# Successful Lead Attributed to Google Ad
Xenon().leadAttributed(source)
#...
# Successful Lead Attributed to Google Search Ad
Xenon().leadAttributed(source, identifier)
```

<br/>

#### Lead Capture  <a id='ecom-lead-capture'></a>
Use this call to track Lead Capture (emails, phone numbers, etc.)
You can add a specifier string to the call to differentiate as follows:

<br/>

##### ```leadCaptured()```
```python
from xenon_view_sdk import Xenon

emailSpecified = "Email"
phoneSpecified = "Phone Number"

# Successful Lead Capture of an email
Xenon().leadCaptured(emailSpecified)
# ...
# Successful Lead Capture of a phone number
Xenon().leadCaptured(phoneSpecified)
```

<br/>

##### ```leadCaptureDeclined()``` <a id='ecom-lead-capture-fail'></a>
> :memo: Note: You want to be consistent between success and failure and match the specifiers
```python
from xenon_view_sdk import Xenon

emailSpecified = "Email"
phoneSpecified = "Phone Number" 

# Unsuccessful Lead Capture of an email
Xenon().leadCaptureDeclined(emailSpecified)
# ...
# Unsuccessful Lead Capture of a phone number
Xenon().leadCaptureDeclined(phoneSpecified)
```

<br/>

#### Account Signup  <a id='ecom-account-signup'></a>
Use this call to track when customers signup for an account.
You can add a specifier string to the call to differentiate as follows:

<br/>

##### ```accountSignup()```
```python
from xenon_view_sdk import Xenon

viaFacebook = "Facebook"
viaGoogle = "Facebook"
viaEmail = "Email"

# Successful Account Signup with Facebook
Xenon().accountSignup(viaFacebook)
# ...
# Successful Account Signup with Google
Xenon().accountSignup(viaGoogle)
# ...
# Successful Account Signup with an Email
Xenon().accountSignup(viaEmail)
```

<br/>

##### ```accountSignupDeclined()``` <a id='ecom-account-signup-fail'></a>
> :memo: Note: You want to be consistent between success and failure and match the specifiers
```python
from xenon_view_sdk import Xenon

viaFacebook = "Facebook"
viaGoogle = "Facebook"
viaEmail = "Email"

# Unsuccessful Account Signup with Facebook
Xenon().accountSignupDeclined(viaFacebook)
# ...
# Unsuccessful Account Signup with Google
Xenon().accountSignupDeclined(viaGoogle)
# ...
# Unsuccessful Account Signup with an Email
Xenon().accountSignupDeclined(viaEmail)
```

<br/>

#### Add Product To Cart  <a id='ecom-product-to-cart'></a>
Use this call to track when customers add a product to the cart.
You can add a specifier string to the call to differentiate as follows:

<br/>

##### ```productAddedToCart()```
```python
from xenon_view_sdk import Xenon

laptop = "Dell XPS"
keyboard = "Apple Magic Keyboard"

# Successful adds a laptop to the cart
Xenon().productAddedToCart(laptop)
# ...
# Successful adds a keyboard to the cart
Xenon().productAddedToCart(keyboard)
```

<br/>

##### ```productNotAddedToCart()``` <a id='ecom-product-to-cart-fail'></a>
> :memo: Note: You want to be consistent between success and failure and match the specifiers
```python
from xenon_view_sdk import Xenon

laptop = "Dell XPS"
keyboard = "Apple Magic Keyboard"

# Doesn't add a laptop to the cart
Xenon().productNotAddedToCart(laptop)
# ...
# Doesn't add a keyboard to the cart
Xenon().productNotAddedToCart(keyboard)
```

<br/>

#### Upsold Additional Products  <a id='ecom-upsell'></a>
Use this call to track when you upsell additional product(s) to customers.
You can add a specifier string to the call to differentiate as follows:

<br/>

##### ```upsold()```
```python
from xenon_view_sdk import Xenon

laptop = 'Dell XPS'
laptopValue = '$1459' #optional
keyboard = 'Apple Magic Keyboard'
keyboardValue = '$139' #optional

# upsold a laptop
Xenon().upsold(laptop)
# ...
# upsold a keyboard with price
Xenon().upsold(keyboard, keyboardValue)
```

<br/>

##### ```upsellDismissed()``` <a id='ecom-upsell-fail'></a>
> :memo: Note: You want to be consistent between success and failure and match the specifiers
```python
from xenon_view_sdk import Xenon

laptop = 'Dell XPS'
keyboard = 'Apple Magic Keyboard'
keyboardValue = '$139' #optional

# Doesn't add a laptop during upsell
Xenon().upsellDismissed(laptop)
# ...
# Doesn't add a keyboard during upsell
Xenon().upsellDismissed(keyboard, keyboardValue)
```

<br/>

#### Customer Checks Out  <a id='ecom-checkout'></a>
Use this call to track when your Customer is checking out.

<br/>

##### ```checkedOut()```
```python
from xenon_view_sdk import Xenon

# Successful Checkout
Xenon().checkedOut()
```

<br/>

##### ```checkoutCanceled()``` <a id='ecom-checkout-fail'></a>
```python
from xenon_view_sdk import Xenon

# Customer cancels check out.
Xenon().checkoutCanceled()

```

<br/>

##### ```productRemoved()``` <a id='ecom-checkout-remove'></a>
```python
from xenon_view_sdk import Xenon

laptop = "Dell XPS"
keyboard = "Apple Magic Keyboard"

# Removes a laptop during checkout
Xenon().productRemoved(laptop)
# ...
# Removes a keyboard during checkout
Xenon().productRemoved(keyboard)
```

<br/>

#### Customer Completes Purchase  <a id='ecom-purchase'></a>
Use this call to track when your Customer completes a purchase.

<br/>

##### ```purchased()```
```python
from xenon_view_sdk import Xenon

method = "Stripe"
price = '$2011' # optional

# Successful Purchase
Xenon().purchased(method)

# Successful Purchase for $2011
Xenon().purchased(method, price)
```

<br/>

##### ```purchaseCanceled()``` <a id='ecom-purchase-fail'></a>
```python
from xenon_view_sdk import Xenon

method = "Stripe" #optional
price = '$2011' # optional

# Customer cancels the purchase.
Xenon().purchaseCanceled()
# -OR-
Xenon().purchaseCanceled(method)
# -OR-
Xenon().purchaseCanceled(method, price)
```

<br/>

#### Purchase Shipping  <a id='ecom-promise-fulfillment'></a>
Use this call to track when your Customer receives a purchase.

<br/>

##### ```promiseFulfilled()```
```python
from xenon_view_sdk import Xenon

# Successfully Delivered Purchase
Xenon().promiseFulfilled()
```

<br/>

##### ```promiseUnfulfilled(()``` <a id='ecom-promise-fulfillment-fail'></a>
```python
from xenon_view_sdk import Xenon

# Problem Occurs During Shipping And No Delivery
Xenon().promiseUnfulfilled()
```

<br/>

#### Customer Keeps or Returns Product  <a id='ecom-product-outcome'></a>
Use this call to track if your Customer keeps the product.
You can add a specifier string to the call to differentiate as follows:

<br/>

##### ```productKept()```
```python
from xenon_view_sdk import Xenon

laptop = "Dell XPS"
keyboard = "Apple Magic Keyboard"

# Customer keeps a laptop
Xenon().productKept(laptop)
# ...
# Customer keeps a keyboard
Xenon().productKept(keyboard)
```

<br/>

##### ```productReturned()``` <a id='ecom-product-outcome-fail'></a>
> :memo: Note: You want to be consistent between success and failure and match the specifiers
```python
from xenon_view_sdk import Xenon

laptop = "Dell XPS"
keyboard = "Apple Magic Keyboard"

# Customer returns a laptop
Xenon().productReturned(laptop)
# ...
# Customer returns a keyboard
Xenon().productReturned(keyboard)
```

<br/>

#### Referrals  <a id='ecom-referral'></a>
Use this call to track when customers refer someone to your offering.
You can add a specifier string to the call to differentiate as follows:

<br/>

##### ```referral()```
```python
from xenon_view_sdk import Xenon

kind = "Share Product"
detail = "Dell XPS"

# Successful referral by sharing a laptop
Xenon().referral(kind, detail)
```

<br/>

##### ```referralDeclined()``` <a id='ecom-referral-fail'></a>
> :memo: Note: You want to be consistent between success and failure and match the specifiers
```python
from xenon_view_sdk import Xenon

kind = "Share Product"
detail = "Dell XPS"

# Customer declined referral 
Xenon().referralDeclined(kind, detail)
```

<br/>

[back to top](#contents)

### Customer Journey Milestones <a id='milestones'></a>

As a customer interacts with your brand (via Advertisements, Marketing Website, Product/Service, etc.), they journey through a hierarchy of interactions.
At the top level are business outcomes. In between Outcomes, they may achieve other milestones, such as interacting with content and features.
Proper instrumentation of these milestones can establish correlation and predictability of business outcomes.

As of right now, Customer Journey Milestones break down into two categories:
1. [Feature Usage](#feature-usage)
2. [Content Interaction](#content-interaction)

<br/>

#### Feature Usage  <a id='feature-usage'></a>
Features are your product/application/service's traits or attributes that deliver value to your customers.
They differentiate your offering in the market. Typically, they are made up of and implemented by functions.

<br/>

##### ```featureAttempted()``` <a id='feature-started'></a>
Use this function to indicate the start of feature usage.
```python
from xenon_view_sdk import Xenon

name = "Scale Recipe"
detail = "x2"   # optional

# Customer initiated using a feature 
Xenon().featureAttempted(name, detail)
# -OR-
Xenon().featureAttempted(name)
```

<br/>

##### ```featureCompleted()``` <a id='feature-complete'></a>
Use this function to indicate the successful completion of the feature.
```python
from xenon_view_sdk import Xenon

name = "Scale Recipe"
detail = "x2"  # optional
# ...
# Customer used a feature 
Xenon().featureCompleted(name)

# -OR-

# Customer initiated using a feature 
Xenon().featureAttempted(name, detail)
# ...
# feature code/function calls
# ...
# feature completes successfully 
Xenon().featureCompleted(name, detail)
# -OR-
Xenon().featureCompleted(name)
```

<br/>

##### ```featureFailed()``` <a id='feature-failed'></a>
Use this function to indicate the unsuccessful completion of a feature being used (often in the exception handler).
```python
from xenon_view_sdk import Xenon


name = "Scale Recipe"
detail = "x2"  # optional


# Customer initiated using a feature 
Xenon().featureAttempted(name, detail)
try:
    # feature code that could fail
except Exception as e:
    # feature completes unsuccessfully 
    Xenon().featureFailed(name, detail)
    # -OR-
    Xenon().featureFailed(name)
```

<br/>

[back to top](#contents)

#### Content Interaction  <a id='content-interaction'></a>
Content is created assets/resources for your site/service/product.
It can be static or dynamic. You will want to mark content that contributes to your Customer's experience or buying decision.
Typical examples:
* Blog
* Blog posts
* Video assets
* Comments
* Reviews
* HowTo Guides
* Charts/Graphs
* Product/Service Descriptions
* Surveys
* Informational product

<br/>

##### ```contentViewed()``` <a id='content-viewed'></a>
Use this function to indicate a view of specific content.
```python
from xenon_view_sdk import Xenon

contentType = "Blog Post"
identifier = "how-to-install-xenon-view" # optional

# Customer view a blog post 
Xenon().contentViewed(contentType, identifier)
# -OR-
Xenon().contentViewed(contentType)
```

<br/>

##### ```contentEdited()``` <a id='content-edited'></a>
Use this function to indicate the editing of specific content.
```python
from xenon_view_sdk import Xenon

contentType = "Review"
identifier = "Dell XPS" # optional
detail = "Rewrote" # optional

# Customer edited their review about a laptop
Xenon().contentEdited(contentType, identifier, detail)
# -OR-
Xenon().contentEdited(contentType, identifier)
# -OR-
Xenon().contentEdited(contentType)
```

<br/>

##### ```contentCreated()``` <a id='content-created'></a>
Use this function to indicate the creation of specific content.
```python
from xenon_view_sdk import Xenon

contentType = "Blog Comment"
identifier = "how-to-install-xenon-view" # optional

# Customer wrote a comment on a blog post
Xenon().contentCreated(contentType, identifier)
# -OR- 
Xenon().contentCreated(contentType)
```

<br/>

##### ```contentDeleted()``` <a id='content-deleted'></a>
Use this function to indicate the deletion of specific content.
```python
from xenon_view_sdk import Xenon

contentType = "Blog Comment"
identifier = "how-to-install-xenon-view" # optional

# Customer deleted their comment on a blog post 
Xenon().contentDeleted(contentType, identifier)
# -OR- 
Xenon().contentDeleted(contentType)
```

<br/>

##### ```contentArchived()``` <a id='content-archived'></a>
Use this function to indicate archiving specific content.
```python
from xenon_view_sdk import Xenon

contentType = "Blog Comment"
identifier = "how-to-install-xenon-view" # optional

# Customer archived their comment on a blog post 
Xenon().contentArchived(contentType, identifier)
# -OR- 
Xenon().contentArchived(contentType)
```

<br/>

##### ```contentRequested()``` <a id='content-requested'></a>
Use this function to indicate the request for specific content.
```python
from xenon_view_sdk import Xenon

contentType = "Info Product"
identifier = "how-to-efficiently-use-google-ads" # optional

# Customer requested some content
Xenon().contentRequested(contentType, identifier)
# -OR- 
Xenon().contentRequested(contentType)
```

<br/>

##### ```contentSearched()``` <a id='content-searched'></a>
Use this function to indicate when a user searches.
```python
from xenon_view_sdk import Xenon

contentType = "Info Product"

# Customer searched for some content
Xenon().contentSearched(contentType)
```


<br/>

[back to top](#contents)

### Commit Points   <a id='commiting'></a>


Business Outcomes and Customer Journey Milestones are tracked locally in memory until you commit them to the Xenon View system.
After you have created (by either calling a milestone or outcome) a customer journey, you can commit it to Xenon View for analysis as follows:

<br/>

#### `commit()`
```python
from xenon_view_sdk import Xenon

# you can commit a journey to Xenon View
Xenon().commit()
```
This call commits a customer journey to Xenon View for analysis.



<br/>

[back to top](#contents)

### Heartbeats   <a id='heartbeat'></a>


Business Outcomes and Customer Journey Milestones are tracked locally in memory until you commit them to the Xenon View system.
You can use the heartbeat call if you want to commit in batch.

The heartbeat call will update a last-seen metric for customer journeys that have yet to arrive at Business Outcome. 
The last-seen metric is useful when analyzing stalled Customer Journeys.

Usage is as follows:

<br/>

#### `heartbeat()`
```python
from xenon_view_sdk import Xenon

# you can heartbeat to Xenon View
Xenon().heartbeat()
```
This call commits any uncommitted journeys to Xenon View for analysis and updates the last accessed time.

> **:memo: Note:** Optionally, you can set abandonment timers via the watchdog parameter. This will allow you to indicate the failed to 
reach outcomes if no activity is recorded before a specified timeout. 

Usage is as follows:

<br/>

#### `heartbeat(watchdog={params})`
```python
from xenon_view_sdk import Xenon

# you can set up an abandonment watchdog
Xenon().heartbeat(watchdog={
        'if_abandoned': {
            'superOutcome': 'Checkout',
            'outcome': 'abandoned',
            'result': 'fail'
        },
        'expires_in_seconds': 600, #10-mins
    })

# you can remove an active watchdog
Xenon().heartbeat(watchdog={
        'remove': True
    })
```


<br/>

[back to top](#contents)

### Platforming  <a id='platforming'></a>

After you have initialized Xenon View, you can optionally specify platform details such as:

- Operating System Name
- Operating System version
- Device model (Pixel, Docker Container, Linux VM, Dell Server, etc.)
- A software version of your application.

<br/>

#### `platform()`
```python
from xenon_view_sdk import Xenon

softwareVersion = "5.1.5"
deviceModel = "Pixel 4 XL"
operatingSystemVersion = "12.0"
operatingSystemName = "Android"

# you can add platform details to outcomes
Xenon().platform(softwareVersion, deviceModel, operatingSystemName, operatingSystemVersion)
```
This adds platform details for each outcome ([Saas](#saas)/[Ecom](#ecom)). Typically, this would be set once at initialization:
```python
from xenon_view_sdk import Xenon

Xenon().init('<API KEY>')
softwareVersion = "5.1.5"
deviceModel = "Pixel 4 XL"
operatingSystemVersion = "12.0"
operatingSystemName = "Android"
Xenon().platform(softwareVersion, deviceModel, operatingSystemName, operatingSystemVersion)
```
<br/>

[back to top](#contents)

### Experiments  <a id="experiments"></a>

After you have initialized Xenon View, you can optionally name variants of customer journeys.
Named variants facilitate running experiments such as A/B or split testing.

> :memo: Note: You are not limited to just 2 (A or B); there can be many. Additionally, you can have multiple variant names.

<br/>

#### `variant()`
```python
from xenon_view_sdk import Xenon

variant = "subscription-variant-A"

# you can add variant details to outcomes
Xenon().variant([variant])
```
This adds variant names to each outcome while the variant in play ([Saas](#saas)/[Ecom](#ecom)).
Typically, you would name a variant once you know the active experiment for this Customer:
```python
from xenon_view_sdk import Xenon

Xenon().init('<API KEY>')
experimentName = getExperiment()
Xenon().variant([experimentName])
```
<br/>

#### `resetVariants()`
```python
from xenon_view_sdk import Xenon

# you can clear all variant names with the resetVariants method
Xenon().resetVariants()
```
<br/>

[back to top](#contents)

### Customer Journey Grouping <a id='deanonymizing-journeys'></a>


Xenon View supports both anonymous and grouped (known) journeys.

All the customer journeys (milestones and outcomes) are anonymous by default.
For example, if a Customer interacts with your brand in the following way:
1. Starts on your marketing website.
2. Downloads and uses an app.
3. Uses a feature requiring an API call.

*Each of those journeys will be unconnected and not grouped.*

To associate those journeys with each other, you can use `deanonymize()`. Deanonymizing will allow for a deeper analysis of a particular user.

Deanonymizing is optional. Basic matching of the customer journey with outcomes is valuable by itself. Deanonymizing will add increased insight as it connects Customer Journeys across devices.

Usage is as follows:

<br/>

#### `deanonymize()`
```python
from xenon_view_sdk import Xenon

# you can deanonymize before or after you have committed the journey (in this case, after):
person = {
    'name': 'Python Testing',
    'email': 'pytest@example.com'
}
Xenon().deanonymize(person)

# you can also deanonymize with a user ID:
person = {
    'UUID': "<some unique ID>"
}
Xenon().deanonymize(person)
```
This call deanonymizes every journey committed to a particular user.

> **:memo: Note:** With journeys that span multiple platforms (e.g., Website->Android->API backend), you can group the Customer Journeys by deanonymizing each.


<br/>

[back to top](#contents)

### Other Operations <a id='other'></a>

There are various other operations that you might find helpful:

<br/>
<br/>

#### Error handling <a id='errors'></a>
In the event of an API error, an exception occurs with the response from the API as [Requests response object](https://docs.python-requests.org/en/latest/user/quickstart/#response-content):

> **:memo: Note:** The default handling of this situation will restore the journey (appending newly added pageViews, events, etc.) for future committing. If you want to do something special, you can do so like this:

```python
from xenon_view_sdk import Xenon, ApiException

try:
    Xenon().commit()

except ApiException as e:
    print(str(e.apiResponse().status_code))
```

<br/>

#### Custom Milestones <a id='custom'></a>

You can add custom milestones if you need more than the current Customer Journey Milestones.

<br/>

##### `milestone()`
```python
from xenon_view_sdk import Xenon

# you can add a custom milestone to the customer journey
category = "Function"
operation = "Called"
name = "Query Database"
detail = "User Lookup"
Xenon().milestone(category, operation, name, detail)
```
This call adds a custom milestone to the customer journey.

<br/>

#### Journey IDs <a id='cuuid'></a>
Each Customer Journey has an ID akin to a session.
After committing an Outcome, the ID remains the same to link all the Journeys.
If you have a previous Customer Journey in progress and would like to append to that, you can get/set the ID.

> **:memo: Note:** For Python, the Xenon object is a singleton. Subsequent Outcomes for multiple threads or async operations will reuse the Journey ID.

After you have initialized the Xenon singleton, you can:
1. Use the default UUID
2. Set the Customer Journey (Session) ID
3. Regenerate a new UUID
4. Retrieve the Customer Journey (Session) ID

<br/>

##### `id()`
```python
from xenon_view_sdk import Xenon

# by default has Journey ID
print(str(Xenon().id()))

# you can also set the id
testId = '<some random uuid>'
Xenon().id(testId)
assert Xenon().id() == testId

# Lastly, you can generate a new Journey ID (useful for serialized async operations that are for different customers)
Xenon().newId()
```
<br/>

[back to top](#contents)

#### Augment Calls with URL <a id='augment-calls'></a>

To track where milestones and outcomes occur, you can augment every call with a URL. 
Call this function to set the URL of the page. Each call afterward will have the URL
attached.

<br/>

##### `pageURL()`
```python
from xenon_view_sdk import Xenon

# you can augment future calls with the page URL
url = 'https://example.com'
Xenon().pageURL(url)
```

<br/>

[back to top](#contents)

<br/>

[back to top](#contents)

## License  <a name="license"></a>

Apache Version 2.0

See [LICENSE](https://github.com/xenonview-com/view-js-sdk/blob/main/LICENSE)

[back to top](#contents)

