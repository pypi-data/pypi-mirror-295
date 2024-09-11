'''
Created on September 20, 2021
@author: lwoydziak
'''
from mockito.matchers import Contains
from pytest import raises

from xenon_view_sdk import Xenon


def setup_function(function):
    Xenon._instance = None


def teardown_function(function):
    Xenon._instance = None


# Platforming, Tagging and Init tests


def test_cannotCreateView():
    with raises(ValueError) as e:
        Xenon()
    assert Contains('Xenon should be initialized with an API Key from XenonView.').matches(str(e.exconly()))


def test_canChangeViewApiKey():
    Xenon(apiKey='<API KEY>', apiUrl='<url>')
    newApiKey = 'new'
    Xenon().key(newApiKey)
    assert newApiKey == Xenon().key()


def test_canAddOutcomeWithPlatformReset():
    Xenon(apiKey='<API KEY>')
    softwareVersion = "5.1.5"
    deviceModel = "Pixel 4 XL"
    operatingSystemName = "Android"
    operatingSystemVersion = "12.0"
    Xenon().platform(softwareVersion, deviceModel, operatingSystemName, operatingSystemVersion)
    Xenon().removePlatform()
    Xenon().applicationInstalled()
    journey = Xenon().journey()[0]
    assert 'platform' not in journey.keys()


def test_canAddOutcomeWithPlatform():
    Xenon(apiKey='<API KEY>')
    softwareVersion = "5.1.5"
    deviceModel = "Pixel 4 XL"
    operatingSystemName = "Android"
    operatingSystemVersion = "12.0"
    Xenon().platform(softwareVersion, deviceModel, operatingSystemName, operatingSystemVersion)
    Xenon().applicationInstalled()
    journey = Xenon().journey()[0]
    assert journey['platform'] == {
        "softwareVersion": softwareVersion,
        "deviceModel": deviceModel,
        "operatingSystemName": operatingSystemName,
        "operatingSystemVersion": operatingSystemVersion
    }


def test_canAddOutcomeWithTagsReset():
    Xenon(apiKey='<API KEY>')
    variants = ["variant"]
    Xenon().variant(variants)
    Xenon().resetVariants()
    Xenon().applicationInstalled()
    journey = Xenon().journey()[0]
    assert 'tags' not in journey.keys()


def test_canAddOutcomeWithTags():
    Xenon(apiKey='<API KEY>')
    variants = ["variant"]
    Xenon().variant(variants)
    Xenon().applicationInstalled()
    journey = Xenon().journey()[0]
    assert journey['tags'] == variants


# Stock Business Outcomes tests

def test_canAttributeLeads():
    Xenon(apiKey='<API KEY>')
    source = 'Google Ad'
    identifier = 'Search'
    Xenon().leadAttributed(source, identifier)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Lead Attributed'
    assert journey['outcome'] == source
    assert journey['id'] == identifier
    assert journey['result'] == 'success'


def test_canAttributeLeadsWithoutId():
    Xenon(apiKey='<API KEY>')
    source = 'Google Ad'
    Xenon().leadAttributed(source)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Lead Attributed'
    assert journey['outcome'] == source
    assert 'id' not in journey.keys()
    assert journey['result'] == 'success'


def test_canCaptureLeads():
    Xenon(apiKey='<API KEY>')
    emailSpecified = "Email"
    Xenon().leadCaptured(emailSpecified)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Lead Capture'
    assert journey['outcome'] == emailSpecified
    assert journey['result'] == 'success'


def test_cannotCaptureLeads():
    Xenon(apiKey='<API KEY>')
    emailSpecified = "Email"
    Xenon().leadCaptureDeclined(emailSpecified)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Lead Capture'
    assert journey['outcome'] == emailSpecified
    assert journey['result'] == 'fail'


def test_canAccountSignup():
    Xenon(apiKey='<API KEY>')
    viaFacebook = "Facebook"
    Xenon().accountSignup(viaFacebook)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Account Signup'
    assert journey['outcome'] == viaFacebook
    assert journey['result'] == 'success'


def test_cannotAccountSignup():
    Xenon(apiKey='<API KEY>')
    viaFacebook = "Facebook"
    Xenon().accountSignupDeclined(viaFacebook)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Account Signup'
    assert journey['outcome'] == viaFacebook
    assert journey['result'] == 'fail'


def test_canInstallApplication():
    Xenon(apiKey='<API KEY>')
    Xenon().applicationInstalled()
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Application Installation'
    assert journey['outcome'] == 'Installed'
    assert journey['result'] == 'success'


def test_cannotInstallApplication():
    Xenon(apiKey='<API KEY>')
    Xenon().applicationNotInstalled()
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Application Installation'
    assert journey['outcome'] == 'Not Installed'
    assert journey['result'] == 'fail'


def test_canInitiallySubscribe():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    Xenon().initialSubscription(annualSilver, method)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Initial Subscription'
    assert journey['outcome'] == 'Subscribe - Silver Annual'
    assert journey['result'] == 'success'


def test_canInitiallySubscribeWithPrice():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    price = '$25'
    Xenon().initialSubscription(annualSilver, method, price)
    journey = Xenon().journey()[0]
    assert journey['price'] == price


def test_canInitiallySubscribeWithTerm():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    term = '30d'
    Xenon().initialSubscription(annualSilver, method, term=term)
    journey = Xenon().journey()[0]
    assert journey['term'] == term


def test_cannotInitiallySubscribe():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    Xenon().subscriptionDeclined(annualSilver, method)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Initial Subscription'
    assert journey['outcome'] == 'Decline - Silver Annual'
    assert journey['result'] == 'fail'


def test_cannotInitiallySubscribeWithPrice():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    price = '$25'
    Xenon().subscriptionDeclined(annualSilver, method, price)
    journey = Xenon().journey()[0]
    assert journey['price'] == price


def test_cannotInitiallySubscribeWithTerm():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    term = '30d'
    Xenon().subscriptionDeclined(annualSilver, method, term=term)
    journey = Xenon().journey()[0]
    assert journey['term'] == term


def test_canRenewSubscription():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    Xenon().subscriptionRenewed(annualSilver, method)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Subscription Renewal'
    assert journey['outcome'] == 'Renew - Silver Annual'
    assert journey['result'] == 'success'


def test_canRenewSubscriptionWithPrice():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    price = '$25'
    Xenon().subscriptionRenewed(annualSilver, method, price)
    journey = Xenon().journey()[0]
    assert journey['price'] == price


def test_canRenewSubscriptionWithTerm():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    term = '30d'
    Xenon().subscriptionRenewed(annualSilver, method, term=term)
    journey = Xenon().journey()[0]
    assert journey['term'] == term


def test_cannotRenewSubscription():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    Xenon().subscriptionCanceled(annualSilver, method)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Subscription Renewal'
    assert journey['outcome'] == 'Cancel - Silver Annual'
    assert journey['result'] == 'fail'


def test_cannotRenewSubscriptionWithPrice():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    price = '$25'
    Xenon().subscriptionCanceled(annualSilver, method, price)
    journey = Xenon().journey()[0]
    assert journey['price'] == price


def test_cannotRenewSubscriptionWithTerm():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    term = '30d'
    Xenon().subscriptionCanceled(annualSilver, method, term=term)
    journey = Xenon().journey()[0]
    assert journey['term'] == term


def test_canPauseSubscription():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    Xenon().subscriptionPaused(annualSilver, method)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Subscription Renewal'
    assert journey['outcome'] == 'Paused - Silver Annual'
    assert journey['result'] == 'fail'


def test_canPauseSubscriptionWithPrice():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    price = '$25'
    Xenon().subscriptionPaused(annualSilver, method, price)
    journey = Xenon().journey()[0]
    assert journey['price'] == price


def test_canPauseSubscriptionWithTerm():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    term = '30d'
    Xenon().subscriptionPaused(annualSilver, method, term=term)
    journey = Xenon().journey()[0]
    assert journey['term'] == term


def test_canUpsellSubscription():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    Xenon().subscriptionUpsold(annualSilver, method)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Subscription Upsold'
    assert journey['outcome'] == 'Upsold - Silver Annual'
    assert journey['result'] == 'success'


def test_canUpsellSubscriptionWithPrice():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    price = '$25'
    Xenon().subscriptionUpsold(annualSilver, method, price)
    journey = Xenon().journey()[0]
    assert journey['price'] == price


def test_canUpsellSubscriptionWithTerm():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    term = '30d'
    Xenon().subscriptionUpsold(annualSilver, method, term=term)
    journey = Xenon().journey()[0]
    assert journey['term'] == term


def test_cannotUpsellSubscription():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    Xenon().subscriptionUpsellDeclined(annualSilver, method)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Subscription Upsold'
    assert journey['outcome'] == 'Declined - Silver Annual'
    assert journey['result'] == 'fail'


def test_cannotUpsellSubscriptionWithPrice():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    price = '$25'
    Xenon().subscriptionUpsellDeclined(annualSilver, method, price)
    journey = Xenon().journey()[0]
    assert journey['price'] == price


def test_cannotUpsellSubscriptionWithTerm():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    term = '30d'
    Xenon().subscriptionUpsellDeclined(annualSilver, method, term=term)
    journey = Xenon().journey()[0]
    assert journey['term'] == term


def test_canSubscriptionDownsell():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    Xenon().subscriptionDownsell(annualSilver, method)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Subscription Upsold'
    assert journey['outcome'] == 'Downsell - Silver Annual'
    assert journey['result'] == 'fail'


def test_canSubscriptionDownsellWithPrice():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    price = '$25'
    Xenon().subscriptionDownsell(annualSilver, method, price)
    journey = Xenon().journey()[0]
    assert journey['price'] == price


def test_canSubscriptionDownsellWithTerm():
    Xenon(apiKey='<API KEY>')
    annualSilver = "Silver Annual"
    method = "Stripe"
    term = '30d'
    Xenon().subscriptionDownsell(annualSilver, method, term=term)
    journey = Xenon().journey()[0]
    assert journey['term'] == term


def test_canAdClicked():
    Xenon(apiKey='<API KEY>')
    provider = "AdMod"
    id_ = "ID-1234"
    Xenon().adClicked(provider)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Advertisement'
    assert journey['outcome'] == 'Ad Click - AdMod'
    assert journey['result'] == 'success'


def test_canAdClickedWithPrice():
    Xenon(apiKey='<API KEY>')
    provider = "AdMod"
    id_ = "ID-1234"
    price = '$25'
    Xenon().adClicked(provider, id_, price)
    journey = Xenon().journey()[0]
    assert journey['id'] == id_
    assert journey['price'] == price


def test_canAdIgnored():
    Xenon(apiKey='<API KEY>')
    provider = "AdMod"
    id_ = "ID-1234"
    Xenon().adIgnored(provider)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Advertisement'
    assert journey['outcome'] == 'Ad Ignored - AdMod'
    assert journey['result'] == 'fail'


def test_canAdIgnoredWithPrice():
    Xenon(apiKey='<API KEY>')
    provider = "AdMod"
    id_ = "ID-1234"
    price = '$25'
    Xenon().adIgnored(provider, id_, price)
    journey = Xenon().journey()[0]
    assert journey['id'] == id_
    assert journey['price'] == price


def test_canRefer():
    Xenon(apiKey='<API KEY>')
    kind = "Share"
    detail = "Review"
    Xenon().referral(kind, detail)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Referral'
    assert journey['outcome'] == 'Referred - Share'
    assert journey['result'] == 'success'


def test_cannotRefer():
    Xenon(apiKey='<API KEY>')
    kind = "Share"
    detail = "Review"  # optional
    Xenon().referralDeclined(kind, detail)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Referral'
    assert journey['outcome'] == 'Declined - Share'
    assert journey['result'] == 'fail'


def test_canAddToCart():
    Xenon(apiKey='<API KEY>')
    laptop = "Dell XPS"
    Xenon().productAddedToCart(laptop)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Add Product To Cart'
    assert journey['outcome'] == 'Add - Dell XPS'
    assert journey['result'] == 'success'


def test_cannotAddToCart():
    Xenon(apiKey='<API KEY>')
    laptop = "Dell XPS"
    Xenon().productNotAddedToCart(laptop)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Add Product To Cart'
    assert journey['outcome'] == 'Ignore - Dell XPS'
    assert journey['result'] == 'fail'


def test_canUpsell():
    Xenon(apiKey='<API KEY>')
    laptop = "Dell XPS"
    Xenon().upsold(laptop)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Upsold Product'
    assert journey['outcome'] == 'Upsold - Dell XPS'
    assert journey['result'] == 'success'


def test_cannotUpsell():
    Xenon(apiKey='<API KEY>')
    laptop = "Dell XPS"
    Xenon().upsellDismissed(laptop)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Upsold Product'
    assert journey['outcome'] == 'Dismissed - Dell XPS'
    assert journey['result'] == 'fail'


def test_canCheckOut():
    Xenon(apiKey='<API KEY>')
    Xenon().checkedOut()
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Customer Checkout'
    assert journey['outcome'] == 'Checked Out'
    assert journey['result'] == 'success'


def test_cannotCheckOut():
    Xenon(apiKey='<API KEY>')
    Xenon().checkoutCanceled()
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Customer Checkout'
    assert journey['outcome'] == 'Canceled'
    assert journey['result'] == 'fail'


def test_canRemoveProduct():
    Xenon(apiKey='<API KEY>')
    laptop = "Dell XPS"
    Xenon().productRemoved(laptop)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Customer Checkout'
    assert journey['outcome'] == 'Product Removed - Dell XPS'
    assert journey['result'] == 'fail'


def test_canPurchase():
    Xenon(apiKey='<API KEY>')
    method = "Stripe"
    Xenon().purchased(method)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Customer Purchase'
    assert journey['outcome'] == 'Purchase - Stripe'
    assert journey['result'] == 'success'


def test_canPurchaseWithPrice():
    Xenon(apiKey='<API KEY>')
    method = "Stripe"
    price = '$25'
    Xenon().purchased(method, price)
    journey = Xenon().journey()[0]
    assert journey['price'] == price


def test_cannotPurchase():
    Xenon(apiKey='<API KEY>')
    method = "Stripe"  # optional
    price = '$25'
    Xenon().purchaseCanceled(method, price)
    journey = Xenon().journey()[0]
    assert journey['price'] == price


def test_canFulfillPromise():
    Xenon(apiKey='<API KEY>')
    Xenon().promiseFulfilled()
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Promise Fulfillment'
    assert journey['outcome'] == 'Fulfilled'
    assert journey['result'] == 'success'


def test_cannotFulfillPromise():
    Xenon(apiKey='<API KEY>')
    Xenon().promiseUnfulfilled()
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Promise Fulfillment'
    assert journey['outcome'] == 'Unfulfilled'
    assert journey['result'] == 'fail'


def test_canKeepProduct():
    Xenon(apiKey='<API KEY>')
    laptop = "Dell XPS"
    Xenon().productKept(laptop)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Product Disposition'
    assert journey['outcome'] == 'Kept - Dell XPS'
    assert journey['result'] == 'success'


def test_cannotKeepProduct():
    Xenon(apiKey='<API KEY>')
    laptop = "Dell XPS"
    Xenon().productReturned(laptop)
    journey = Xenon().journey()[0]
    assert journey['superOutcome'] == 'Product Disposition'
    assert journey['outcome'] == 'Returned - Dell XPS'
    assert journey['result'] == 'fail'


# Stock Milestone tests:


def test_canAttemptFeature():
    Xenon(apiKey='<API KEY>')
    name = "Scale Recipe"
    detail = "x2"
    Xenon().featureAttempted(name, detail)
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Feature'
    assert journey['action'] == 'Attempted'
    assert journey['name'] == name
    assert journey['details'] == detail
    assert journey['timestamp'] > 0.0


def test_canCompleteFeature():
    Xenon(apiKey='<API KEY>')
    name = "Scale Recipe"
    detail = "x2"
    Xenon().featureCompleted(name, detail)
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Feature'
    assert journey['action'] == 'Completed'
    assert journey['name'] == name
    assert journey['details'] == detail
    assert journey['timestamp'] > 0.0


def test_canFailFeature():
    Xenon(apiKey='<API KEY>')
    name = "Scale Recipe"
    detail = "x2"
    Xenon().featureFailed(name, detail)
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Feature'
    assert journey['action'] == 'Failed'
    assert journey['name'] == name
    assert journey['details'] == detail
    assert journey['timestamp'] > 0.0


def test_canViewContent():
    Xenon(apiKey='<API KEY>')
    contentType = "Blog Post"
    identifier = "how-to-install-xenon-view"  # optional
    Xenon().contentViewed(contentType, identifier)
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Content'
    assert journey['action'] == 'Viewed'
    assert journey['type'] == contentType
    assert journey['identifier'] == identifier
    assert journey['timestamp'] > 0.0


def test_canEditContent():
    Xenon(apiKey='<API KEY>')
    contentType = "Review"
    identifier = "Dell XPS"  # optional
    detail = "Rewrote"  # optional
    Xenon().contentEdited(contentType, identifier, detail)
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Content'
    assert journey['action'] == 'Edited'
    assert journey['type'] == contentType
    assert journey['identifier'] == identifier
    assert journey['details'] == detail
    assert journey['timestamp'] > 0.0


def test_canCreateContent():
    Xenon(apiKey='<API KEY>')
    contentType = "Blog Comment"
    identifier = "how-to-install-xenon-view"  # optional
    Xenon().contentCreated(contentType, identifier)
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Content'
    assert journey['action'] == 'Created'
    assert journey['type'] == contentType
    assert journey['identifier'] == identifier
    assert journey['timestamp'] > 0.0


def test_canDeleteContent():
    Xenon(apiKey='<API KEY>')
    contentType = "Blog Comment"
    identifier = "how-to-install-xenon-view"  # optional
    Xenon().contentDeleted(contentType, identifier)
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Content'
    assert journey['action'] == 'Deleted'
    assert journey['type'] == contentType
    assert journey['identifier'] == identifier
    assert journey['timestamp'] > 0.0


def test_canArchiveContent():
    Xenon(apiKey='<API KEY>')
    contentType = "Blog Comment"
    identifier = "how-to-install-xenon-view"  # optional
    Xenon().contentArchived(contentType, identifier)
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Content'
    assert journey['action'] == 'Archived'
    assert journey['type'] == contentType
    assert journey['identifier'] == identifier
    assert journey['timestamp'] > 0.0


def test_canRequestContent():
    Xenon(apiKey='<API KEY>')
    contentType = "Info Product"
    identifier = "how-to-efficiently-use-google-ads"  # optional
    Xenon().contentRequested(contentType, identifier)
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Content'
    assert journey['action'] == 'Requested'
    assert journey['type'] == contentType
    assert journey['identifier'] == identifier
    assert journey['timestamp'] > 0.0


def test_canSearchContent():
    Xenon(apiKey='<API KEY>')
    contentType = "Info Product"
    Xenon().contentSearched(contentType)
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Content'
    assert journey['action'] == 'Searched'
    assert journey['type'] == contentType
    assert journey['timestamp'] > 0.0


# Custom Milestones tests


def test_canAddCustomMilestone():
    Xenon(apiKey='<API KEY>')
    category = "Function"
    operation = "Called"
    name = "Query Database"
    detail = "User Lookup"
    Xenon().milestone(category, operation, name, detail)
    journey = Xenon().journey()[0]
    assert journey['category'] == category
    assert journey['action'] == operation
    assert journey['name'] == name
    assert journey['details'] == detail
    assert journey['timestamp'] > 0.0


# Internal tests


def test_doesNotAddDuplicateButIncreasesCountForFeature():
    Xenon(apiKey='<API KEY>')
    name = "Scale Recipe"
    Xenon().featureCompleted(name)
    Xenon().featureCompleted(name)
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Feature'
    assert journey['timestamp'] > 0.0
    assert journey['count'] == 2
    assert len(Xenon().journey()) == 1


def test_doesNotAddDuplicateButIncreasesCountForContent():
    Xenon(apiKey='<API KEY>')
    name = "Recipe"
    Xenon().contentSearched(name)
    Xenon().contentSearched(name)
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Content'
    assert journey['timestamp'] > 0.0
    assert journey['count'] == 2
    assert len(Xenon().journey()) == 1


def test_doesNotAddDuplicateButIncreasesCountForContentWithIdentifier():
    Xenon(apiKey='<API KEY>')
    name = "Recipe"
    Xenon().contentEdited(name, 'identifier')
    Xenon().contentEdited(name, 'identifier')
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Content'
    assert journey['timestamp'] > 0.0
    assert journey['count'] == 2
    assert len(Xenon().journey()) == 1


def test_doesNotAddDuplicateButIncreasesCountForContentWithDetail():
    Xenon(apiKey='<API KEY>')
    name = "Recipe"
    Xenon().contentEdited(name, 'identifier', 'detail')
    Xenon().contentEdited(name, 'identifier', 'detail')
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Content'
    assert journey['timestamp'] > 0.0
    assert journey['count'] == 2
    assert len(Xenon().journey()) == 1


def test_doesNotAddDuplicateButIncreasesCountForCustom():
    Xenon(apiKey='<API KEY>')
    category = "Function"
    operation = "Called"
    name = "Query Database"
    detail = "User Lookup"
    Xenon().milestone(category, operation, name, detail)
    Xenon().milestone(category, operation, name, detail)
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Function'
    assert journey['timestamp'] > 0.0
    assert journey['count'] == 2
    assert len(Xenon().journey()) == 1


def test_doesAddAlmostDuplicateForFeature():
    Xenon(apiKey='<API KEY>')
    name = "Scale Recipe"
    Xenon().featureAttempted(name)
    Xenon().featureCompleted(name)
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Feature'
    assert journey['timestamp'] > 0.0
    assert len(Xenon().journey()) == 2


def test_doesAddAlmostDuplicateForContent():
    Xenon(apiKey='<API KEY>')
    name = "Scale Recipe"
    Xenon().contentViewed(name)
    Xenon().contentSearched(name)
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Content'
    assert journey['timestamp'] > 0.0
    assert len(Xenon().journey()) == 2


def test_doesAddAlmostDuplicateForContentWithIdentifier():
    Xenon(apiKey='<API KEY>')
    name = "Scale Recipe"
    Xenon().contentEdited(name, 'identifier')
    Xenon().contentEdited(name, 'identifier2')
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Content'
    assert journey['timestamp'] > 0.0
    assert len(Xenon().journey()) == 2


def test_doesAddAlmostDuplicateForContentWithDetail():
    Xenon(apiKey='<API KEY>')
    name = "Scale Recipe"
    Xenon().contentEdited(name, 'identifier', 'detail')
    Xenon().contentEdited(name, 'identifier', 'detail2')
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Content'
    assert journey['timestamp'] > 0.0
    assert len(Xenon().journey()) == 2


def test_doesAddAlmostDuplicateForCustom():
    Xenon(apiKey='<API KEY>')
    category = "Function"
    operation = "Called"
    name = "Query Database"
    detail = "User Lookup"
    Xenon().milestone(category, operation, name, detail)
    Xenon().milestone(category, operation, name, detail + '2')
    journey = Xenon().journey()[0]
    assert journey['category'] == 'Function'
    assert journey['timestamp'] > 0.0
    assert len(Xenon().journey()) == 2


def test_addMultipleMilestones():
    Xenon(apiKey='<API KEY>')
    name = "Scale Recipe"
    Xenon().featureAttempted(name)
    Xenon().featureCompleted(name)
    step1 = Xenon().journey()[0]
    step2 = Xenon().journey()[1]
    assert step1['action'] == 'Attempted'
    assert step2['action'] == 'Completed'
    assert step2['timestamp'] > step1['timestamp']


def test_addMilestoneAndOutcome():
    Xenon(apiKey='<API KEY>')
    name = "Scale Recipe"
    tier = "Gold Monthly"
    Xenon().featureAttempted(name)
    Xenon().initialSubscription(tier)
    step1 = Xenon().journey()[0]
    step2 = Xenon().journey()[1]
    assert step1['action'] == 'Attempted'
    assert step2['outcome'] == 'Subscribe - ' + tier
    assert step2['timestamp'] > step1['timestamp']


def test_whenResettingAddingMilestoneAndRestoringRestoredJourneyHasNewMilestone():
    Xenon(apiKey='<API KEY>')
    name = "Scale Recipe"
    Xenon().featureAttempted(name)
    Xenon().reset()
    Xenon().featureCompleted(name)
    Xenon().restore()
    step1 = Xenon().journey()[0]
    step2 = Xenon().journey()[1]
    assert step1['action'] == 'Attempted'
    assert step2['action'] == 'Completed'
    assert step2['timestamp'] > step1['timestamp']


def test_canGetAndSetId():
    Xenon(apiKey='<API KEY>')
    assert Xenon().id() is not None and Xenon().id() != ''
    Xenon().id('test')
    assert Xenon().id() == 'test'


def test_canRegenerateId():
    Xenon(apiKey='<API KEY>')
    previousId = Xenon().id()
    Xenon().newId()
    assert Xenon().id() != previousId
