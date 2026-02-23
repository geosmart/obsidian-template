# Sequence Diagram Complete Reference

Complete syntax for mermaid sequence diagrams.

---

## Declaration

```mermaid
sequenceDiagram
```

---

## Participants

### Basic Definition

```mermaid
sequenceDiagram
    participant A
    participant B
```

### With Aliases

```mermaid
sequenceDiagram
    participant A as Alice
    participant B as Bob
    participant S as Server
```

### Actor (Stick Figure)

```mermaid
sequenceDiagram
    actor User
    participant System

    User->>System: Request
```

---

## Messages

### Arrow Types

```mermaid
sequenceDiagram
    A->>B: Solid arrow
    A-->>B: Dotted arrow
    A-)B: Async message
    A--)B: Async dotted
```

### Arrow Directions

```mermaid
sequenceDiagram
    A->>+B: Activate
    B-->>-A: Deactivate
    A<<->>B: Bidirectional
```

### Without Arrows

```mermaid
sequenceDiagram
    A-B: Solid line
    A--B: Dotted line
```

---

## Activation/Deactivation

```mermaid
sequenceDiagram
    A->>+B: activate B
    B->>+C: activate C
    C-->>-B: deactivate C
    B-->>-A: deactivate B
```

---

## Notes

### Position

```mermaid
sequenceDiagram
    participant A
    participant B

    Note right of A: Right note
    Note left of B: Left note
    Note over A: Over A
    Note over A,B: Spanning note
```

### Multiline Notes

```mermaid
sequenceDiagram
    Note over A,B: Line 1<br/>Line 2<br/>Line 3
```

---

## Loops and Alternatives

### Loop

```mermaid
sequenceDiagram
    loop Every minute
        A->>B: Ping
        B->>A: Pong
    end
```

### Alt (If-else)

```mermaid
sequenceDiagram
    alt Success
        A->>B: OK
    else Failure
        A->>B: Error
    end
```

### Opt (Optional)

```mermaid
sequenceDiagram
    opt Extra step
        A->>B: Optional message
    end
```

### Par (Parallel)

```mermaid
sequenceDiagram
    par Alice to Bob
        A->>B: Message 1
    and Alice to Charlie
        A->>C: Message 2
    end
```

---

## Background Highlighting

### Rect

```mermaid
sequenceDiagram
    rect rgb(200, 220, 250)
        A->>B: In blue box
        B->>C: Also in blue
    end

    rect rgba(200, 250, 200, 0.5)
        C->>A: In green box
    end
```

---

## Autonumbering

```mermaid
sequenceDiagram
    autonumber

    A->>B: First (1)
    B->>C: Second (2)
    C->>A: Third (3)
```

---

## Special Features

### Critical Section

```mermaid
sequenceDiagram
    critical Establish connection
        A->>B: Connect
    option Timeout
        A->>A: Reconnect
    end
```

### Break

```mermaid
sequenceDiagram
    A->>B: Request
    break Error occurred
        B->>A: Error response
    end
```

---

## Sequence Numbers

```mermaid
sequenceDiagram
    autonumber 1 1  %% Start at 1, increment by 1
    A->>B: Message 1
    B->>C: Message 2
```

---

## Links and Styling

### Participant Links

```mermaid
sequenceDiagram
    participant A
    link A: Dashboard @ https://example.com
    link A: Details @ https://example.com/details
```

### Styling

```mermaid
sequenceDiagram
    participant A
    participant B

    A->>B: Message

    style A fill:#bbf
```

---

## Common Patterns

### Request-Response

```mermaid
sequenceDiagram
    Client->>Server: Request
    Server-->>Client: Response
```

### Error Handling

```mermaid
sequenceDiagram
    A->>B: Request
    alt Success
        B->>A: Data
    else Error
        B->>A: Error message
    end
```

### Async Operations

```mermaid
sequenceDiagram
    A-)B: Async call
    Note over B: Processing...
    B--)A: Callback
```

---

## Best Practices

1. **Use aliases:** `participant A as Alice` for readability
2. **Activation:** Use `+`/`-` for clear lifelines
3. **Notes:** Add context for complex flows
4. **Grouping:** Use rect for related operations
5. **Autonumber:** For step-by-step flows

---

## Errors to Avoid

1. **Don't use flowchart syntax:**
   - ❌ `A[Rectangle]` (flowchart syntax)
   - ✅ `participant A` (sequence syntax)

2. **Special chars in messages:**
   - ❌ `A->>B: method()`
   - ✅ `A->>B: method call`

3. **Missing participant:**
   - Define all participants before using

---

## Complete Example

```mermaid
sequenceDiagram
    autonumber
    actor User
    participant App
    participant Server
    participant DB

    User->>+App: Login request
    App->>+Server: Authenticate

    alt Valid credentials
        Server->>+DB: Query user
        DB-->>-Server: User data
        Server-->>App: Token
        App-->>-User: Success
    else Invalid credentials
        Server-->>App: Error
        App-->>-User: Login failed
    end

    Note over User,DB: Authentication complete
```

---

Return to [SKILL.md](SKILL.md)
