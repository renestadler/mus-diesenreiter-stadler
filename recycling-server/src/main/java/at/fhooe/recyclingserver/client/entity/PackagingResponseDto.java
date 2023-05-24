package at.fhooe.recyclingserver.client.entity;

import lombok.Getter;
import lombok.Setter;

@Getter
@Setter
public class PackagingResponseDto {
    private long count;
    private PackagingDto[] tags;
}
