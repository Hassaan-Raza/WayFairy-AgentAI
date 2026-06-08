from crewai import Task


def location_task(agent, from_city, destination_city, date_from, date_to, transport, budget_per_day):
    if transport.lower() == "plane":
        transport_section = f"- Search for flight options from {from_city} to {destination_city}, typical price range and airlines"
    else:
        transport_section = (
            f"- Research {transport} route from {from_city} to {destination_city}: "
            f"distance, estimated travel time, best route, and any tolls or fuel costs"
        )

    return Task(
        description=f"""
You are researching a trip from {from_city} to {destination_city}.
Travel dates: {date_from} to {date_to}
Transport mode: {transport}
Daily budget per person: ${budget_per_day} USD

Your job is to find the following real, specific information:

ACCOMMODATION:
- Find 3 budget-friendly hotels or hostels (under ${int(budget_per_day * 0.4)} per night) with real names and estimated prices
- Find 3 mid-range or nice hotels (${ int(budget_per_day * 0.4)} to ${int(budget_per_day * 0.7)} per night) with real names and estimated prices
- Include neighbourhood location and what each hotel is known for

TRANSPORT:
{transport_section}
- Find local transport options within {destination_city} (metro, bus, taxi, rideshare apps) with approximate costs

PRACTICAL INFO:
- Visa requirements for a traveler coming from {from_city}
- Currency used and approximate exchange rate to USD
- Best areas to stay in {destination_city}
- Any important local customs or safety tips

Write your findings in clear markdown with headers and bullet points.
Include specific prices wherever possible. Label estimates clearly as "(estimated)".
        """,
        expected_output=(
            f"A structured markdown report covering accommodation options with prices, "
            f"transport details from {from_city} to {destination_city}, local transport in {destination_city}, "
            f"visa requirements, currency info, best areas to stay, and practical tips."
        ),
        agent=agent,
        output_file="city_report.md"
    )


def guide_task(agent, destination_city, interests, date_from, date_to, transport, budget_per_day):
    num_days = (date_to - date_from).days + 1

    return Task(
        description=f"""
You are creating a personalized activity guide for {destination_city}.
Trip duration: {num_days} days ({date_from} to {date_to})
Traveler's interests: {interests}
Daily budget per person: ${budget_per_day} USD
Transport within city: {transport}

Your job is to find real, specific activities, restaurants, and experiences that match the traveler's interests.

ACTIVITIES (match to: {interests}):
- Find at least 3 must-do attractions or experiences that match the interests
- Find at least 3 hidden gems or local favorites that match the interests
- For each: name, description, location, opening hours, entry price
- Explain specifically WHY each one suits a traveler interested in {interests}

FOOD & DINING:
- Find 3 restaurants that match the traveler's taste (based on {interests})
- Include one budget option, one mid-range, one special experience
- Give real names, cuisine type, price range per person, and why it is worth visiting

DAY TRIP OPTIONS:
- Suggest 1 or 2 day trip options from {destination_city} if applicable
- Include transport time and rough cost

LOCAL TIPS:
- Best time of day to visit popular spots
- Any seasonal events happening around {date_from} to {date_to}
- Local apps or transport cards useful for getting around

Write everything in clear markdown with specific names and prices.
        """,
        expected_output=(
            f"A personalized guide to {destination_city} with specific attraction names, "
            f"restaurant recommendations, day trip options, and local tips — all tailored to the interests: {interests}."
        ),
        agent=agent,
        output_file="guide_report.md"
    )


def packing_task(agent, destination_city, date_from, date_to, transport, interests, weather_summary):
    num_days = (date_to - date_from).days + 1

    return Task(
        description=f"""
Create a smart, practical packing list for this specific trip.

Trip details:
- Destination: {destination_city}
- Duration: {num_days} days
- Dates: {date_from} to {date_to}
- Transport mode: {transport}
- Activities planned based on interests: {interests}
- Weather forecast summary: {weather_summary}

Create a complete packing list organised by category:

1. CLOTHING — based on weather ({weather_summary}) and planned activities
2. TOILETRIES & HEALTH — essentials only, travel-sized
3. ELECTRONICS & ADAPTERS — based on destination country
4. DOCUMENTS & MONEY — visa, insurance, cards, cash tips
5. TRANSPORT SPECIFIC — items needed for {transport} travel
6. ACTIVITY SPECIFIC — gear for {interests}
7. OPTIONAL BUT USEFUL — nice-to-haves for this specific trip

For each item, add a short note explaining WHY it is needed for this specific trip.
Mark absolute essentials with ⭐
Keep the list realistic — not everything, just what actually matters for this trip.
        """,
        expected_output=(
            f"A categorised, trip-specific packing list for {num_days} days in {destination_city}, "
            f"with items tailored to the weather, activities, and transport mode."
        ),
        agent=agent,
        output_file="packing_list.md"
    )


def planner_task(context, agent, from_city, destination_city, interests, date_from, date_to, transport, budget_per_day):
    num_days = (date_to - date_from).days + 1

    if transport.lower() != "plane":
        transport_note = (
            f"\n\nTRANSPORT SECTION: Since the traveler is going by {transport}, "
            f"include a dedicated section with route details from {from_city} to {destination_city}, "
            f"estimated travel time, recommended stops along the way, and fuel/cost estimates."
        )
    else:
        transport_note = (
            f"\n\nTRANSPORT SECTION: Include flight tips, airport transfer options in {destination_city}, "
            f"and recommended local transport cards or apps."
        )

    return Task(
        description=f"""
Using ONLY the information provided by the location expert and guide expert,
create the final complete Roamio travel plan.

DO NOT search the web. Use only what the experts have already found.

Trip details:
- From: {from_city}
- To: {destination_city}
- Dates: {date_from} to {date_to} ({num_days} days)
- Interests: {interests}
- Transport: {transport}
- Daily budget: ${budget_per_day} per person

Write the complete travel plan in this exact structure:

# 🌍 Welcome to [destination_city]
Write 2 engaging paragraphs introducing the city — its character, what makes it special,
and why it is perfect for someone interested in {interests}.

# 📋 Trip Summary
- From: {from_city}
- To: {destination_city}
- Dates: {date_from} to {date_to}
- Duration: {num_days} days
- Transport: {transport}
- Daily budget: ${budget_per_day} per person
- Interests: {interests}

# 🗓️ Day-by-Day Itinerary
For EACH day from {date_from} to {date_to}, write a full day plan:

## Day [N]: [Date] — [Theme for the day]
**Morning (9:00 AM)**
- Activity: [specific name]
- Why: [why it suits the traveler's interests]
- Cost: [estimate]
- Getting there: [transport details]

**Lunch (12:30 PM)**
- Restaurant: [specific name]
- Cuisine & price: [details]

**Afternoon (2:00 PM)**
- Activity: [specific name]
- Cost: [estimate]

**Evening (7:00 PM)**
- Dinner: [specific restaurant]
- Optional evening activity

**💰 Day [N] Budget Estimate: $[total]**

# 💰 Full Trip Budget Estimate
| Category | Estimated Cost |
|---|---|
| Accommodation ({num_days} nights) | $[amount] |
| Food & dining | $[amount] |
| Activities & entry fees | $[amount] |
| Local transport | $[amount] |
| Shopping & misc | $[amount] |
| **TOTAL ESTIMATE** | **$[total]** |

# 🏨 Recommended Hotels
List the top 3 hotels from the location expert's research with prices.

{transport_note}

# 💡 Roamio Tips
5 practical insider tips for this specific trip.

Use emojis throughout. Write in an engaging, friendly tone.
Make the traveler excited about their trip!
        """,
        expected_output=(
            f"A complete, formatted travel plan for {num_days} days in {destination_city} "
            f"with day-by-day itinerary, budget breakdown, hotel recommendations, "
            f"transport details, and insider tips."
        ),
        context=context,
        agent=agent,
        output_file="travel_plan.md"
    )
